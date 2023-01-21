#include <iostream>
#include <string>
#include <cpr/cpr.h>
#include <windows.h>
#include <lmcons.h>
#include <fstream>
#include <cstdlib>
#include <iterator>
#include <clocale>
#include <stdio.h>

using namespace std;

#pragma region Requests add Computer
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


#pragma endregion

#pragma region Requests data disks pc
list<string> GetHardDrivesPc() {
    DWORD dwSize = MAX_PATH;
    char szLogicalDrives[MAX_PATH] = { 0 };
    DWORD dwResult = GetLogicalDriveStrings(dwSize, szLogicalDrives);

    if (dwResult > 0 && dwResult <= MAX_PATH)
    {
        char* szSingleDrive = szLogicalDrives;
        list<string> data;
        while (*szSingleDrive)
        {
            data.push_back(szSingleDrive);
            szSingleDrive += strlen(szSingleDrive) + 1;
        }
        return data;
    }
}

void RequestAddHardDisk(string url, string name) {
    url.append("pc/client/add_disk/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"name", name},
            {"pc_name", GetNamePc()}
        });

    RequestStatusCode(r.status_code);
}

string SelectSerialNumberDisk(string d) {
    char NameBuffer[MAX_PATH];
    char SysNameBuffer[MAX_PATH];
    DWORD VSNumber;
    DWORD MCLength;
    DWORD FileSF;

    LPCSTR disk = d.append("\\").c_str();

    if (GetVolumeInformation(disk, NameBuffer, sizeof(NameBuffer),
        &VSNumber, &MCLength, &FileSF, SysNameBuffer, sizeof(SysNameBuffer)))
    {

        return to_string(VSNumber);
    }
}

string GetDiskSize(LPCSTR drive)
{
    __int64 totalbytes;
    char buf[255];
    GetDiskFreeSpaceExA(drive, NULL, (PULARGE_INTEGER)&totalbytes, NULL);
    return (to_string(totalbytes));
}

void RequestAddInfoDisk(string url, string disk) {
    url.append("pc/client/info_disk/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"name", disk},
            {"full_name", "KINGSTON"},
            {"serial_number", SelectSerialNumberDisk(disk)},
            {"range", GetDiskSize(disk.c_str()).substr(0,3)}
        });

    RequestStatusCode(r.status_code);
}

void RequestCreateDisks(string url) {
    list<string> data = GetHardDrivesPc();
    for (string disk : data) {
        disk = disk.substr(0, 2);
        RequestAddHardDisk(url, disk);
        RequestAddInfoDisk(url, disk);
    }
}


#pragma endregion


int main()
{
    setlocale(LC_ALL, "Russian");
    string url = "http://127.0.0.1:8000/";
    RequestAddPc(url, GetNamePc(), RequestGetIp(), GetMacAddress(), "Administraton inserting...."); //добавление пк
    RequestCreateDisks(url); // создание дисков

    //SelectHardDiskInfo();
}

