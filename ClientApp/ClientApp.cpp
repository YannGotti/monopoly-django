#include <iostream>
#include <string>
#include <cpr/cpr.h>
#include <windows.h>
#include <lmcons.h>

using namespace std;

void RequestStatusCode(long status_code) {
    if (status_code != 200)
    {
        cout << "Request error";
        return;
    }

    return;
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
    RequestAddPc(url, GetNamePc(), RequestGetIp(), "Asd", "asd");
}

