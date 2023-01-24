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
#include <json/value.h>

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

    LPCSTR disk = d.c_str();

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

    return to_string(totalbytes);
}

string GetDiskFreeSize(LPCSTR drive)
{
    __int64 freebytes;
    char buf[255];
    GetDiskFreeSpaceExA(drive, NULL, NULL, (PULARGE_INTEGER)&freebytes);

    return to_string(freebytes);
}

void RequestAddInfoDisk(string url, string disk) {
    url.append("pc/client/info_disk/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"name", disk},
            {"full_name", "KINGSTON"},
            {"serial_number", SelectSerialNumberDisk(disk)},
            {"free_range", GetDiskFreeSize(disk.c_str()).substr(0, 3)},
            {"range", GetDiskSize(disk.c_str()).substr(0, 3)}
        });

    RequestStatusCode(r.status_code);
}

Json::Value ListToJson(list<string> data)
{
    Json::Value result;

    for (string item : data)
    {
        result.append(item);
    }

    return result;
}

Json::Value SelectCatalogsDisk(string d) {
    WIN32_FIND_DATAW wfd;

    d.append("*");
    wstring stemp = wstring(d.begin(), d.end());
    LPCWSTR disk = stemp.c_str();

    HANDLE const hFind = FindFirstFileW(disk, &wfd);
    setlocale(LC_ALL, "");

    list<string> data;

    if (INVALID_HANDLE_VALUE != hFind)
    {
        do
        {
            wstring ws(&wfd.cFileName[0]);
            string file(ws.begin(), ws.end());

            if (file != ".." && file != ".")
                data.push_back(file);

            
        } while (NULL != FindNextFileW(hFind, &wfd));

        FindClose(hFind);
    }

    return ListToJson(data);
}

void RequestAddCatalogsDisk(string url, string disk) {
    url.append("disk/client/getData/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"path", disk},
            {"data", SelectCatalogsDisk(disk).toStyledString()},
            {"serial_number", SelectSerialNumberDisk(disk)}
        });

    RequestStatusCode(r.status_code);
}

void RequestCreateDisks(string url) {
    list<string> data = GetHardDrivesPc();
    for (string disk : data) {
        RequestAddHardDisk(url, disk);
        RequestAddInfoDisk(url, disk);
        RequestAddCatalogsDisk(url, disk);
    }
}

#pragma endregion

#pragma region AsyncRequests

void RequestUpdateCatalog(string url, string name_disk, string path) {
    url.append("disk/client/getData/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"path", path},
            {"data", SelectCatalogsDisk(path).toStyledString()},
            {"serial_number", SelectSerialNumberDisk(name_disk)}
        });

    RequestStatusCode(r.status_code);
}

void RequestPostState(string url, string disk) {
    url.append("disk/client/postRequestState/");
    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"name_disk", disk},
            {"file_state", "0"},
            {"state", "1"},
        });

    RequestStatusCode(r.status_code);
}

bool IsFile(string path) {
    ifstream f1;

    path = path.substr(0, path.size() - 1);

    f1.open(path);
    if (!(f1.is_open())) {
        return false;
    }
    else {
        f1.close();
        return true;
    }

}

list<string> GetDataFile(string path) {

    list<string> data;

    string line;
    ifstream in(path);
    if (in.is_open())
    {
        while (getline(in, line))
        {
            data.push_back(line += '\n');
        }
    }
    in.close();
    return data;
}

void RequestGetIsFile(string url, string name_disk) {
    url.append("disk/client/requestIsFile/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"name_disk", name_disk},
            {"is_file", "1"}
        });

    RequestStatusCode(r.status_code);
}

void RequestGetFileData(string url, string name_disk, string path, string data_file) {
    url.append("disk/client/GetFileData/");

    auto r = cpr::Get(cpr::Url{ url },
        cpr::Parameters{
            {"name_disk", name_disk},
            {"path", path},
            {"data_file", data_file}
        });

    RequestStatusCode(r.status_code);
}

void RequestPostFileData(string url,string name_disk, string path) {
    list<string> data = GetDataFile(path);
    string data_file;
    Json::Value result;

    for (string line : data)
    {
        data_file.append(line);
    }

    RequestGetIsFile(url, name_disk);
    RequestGetFileData(url, name_disk, path, data_file);
}

void GetRequestServer(string url) {
    string current_url = url;
    current_url.append("disk/client/getRequest/");

    list<string> data = GetHardDrivesPc();
    for (string disk : data) {
        auto r = cpr::Get(cpr::Url{ current_url },
            cpr::Parameters{
                {"name_disk", disk},
            });

        RequestStatusCode(r.status_code);

        string path = r.text;

        if (IsFile(path)) {
            RequestPostFileData(url, disk, path.substr(0, path.size() - 1));
        }

        else {
            RequestUpdateCatalog(url, disk, path);
            RequestPostState(url, disk);
        }
    }
}

void AsyncRequests(string url) {
    for (size_t i = 10; i > 0; i--)
    {

        GetRequestServer(url);
        if (i < 2) i = 10;
        Sleep(3000);
    }
}
#pragma endregion


int main()
{
    string url = "http://127.0.0.1:8000/";
    RequestAddPc(url, GetNamePc(), RequestGetIp(), GetMacAddress(), "Administraton inserting...."); //добавление пк
    RequestCreateDisks(url); // создание дисков

    auto f = async(AsyncRequests, url);
    f.get();

}

