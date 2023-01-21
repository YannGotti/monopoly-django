#include <iostream>
#include <string>
#include <cpr/cpr.h>
#include <windows.h>
#include <lmcons.h>
#include <fstream>
#include <cstdlib>
#include <iterator>

using namespace std;

void RequestStatusCode(long status_code) {
    if (status_code != 200)
    {
        cout << "Request error";
        return;
    }

    return;
}

string GetMacAddress() {
    string cmd = "getmac";
    string filename = "macaddress.txt";

    system((cmd + ">" + filename).c_str());
    string line;
    ifstream myfile("macaddress.txt");

    list<string> data;

    if (myfile.is_open()) {
        int i = 0;
        
        while (getline(myfile, line)) {
            //cout << line << endl;
            data.push_back(line);
            i++;
        }
        myfile.close();
    }
    else {
        cout << "Unable to open the file";
        return "null";
    }
    
    string mac[4];
    int i = 0;
    for (string n : data) {
        mac[i] = n;
        i++;
    }

    return mac[3].substr(0, 17);
}

string GetNamePc() {
    TCHAR pcname[UNCLEN + 1];
    DWORD pcname_len = UNCLEN + 1;

    GetComputerName((TCHAR*)pcname, &pcname_len);

    return pcname;
}

string RequestGetIp() {
    auto r = cpr::Get(cpr::Url{ "http://api.ipify.org/" });
    RequestStatusCode(r.status_code);
    return r.text;
}

void RequestAddPc(string url, string name, string ip, string mac_adress, string description) {
    url.append("pc/client/add_pc/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"name", name},
            {"ip", ip},
            {"mac_adress", mac_adress},
            {"description", description},
        });

    RequestStatusCode(r.status_code);
}

int main()
{
    string url = "http://127.0.0.1:8000/";
    RequestAddPc(url, GetNamePc(), RequestGetIp(), GetMacAddress(), "Заполняется администратором....");
}

