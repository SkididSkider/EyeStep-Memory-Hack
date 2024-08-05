#include <iostream>
#include <Windows.h>
#include <string>
#include <sstream>

std::string App = "Nul";
std::string Adress = "Nul";
std::string Value = "Nul";

using namespace std;

void SetConsoleTextColor(int color) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, color);
}

int main() {
    SetConsoleTextColor(4);
    cout << "EyeStep(C++ BETA)" << '\n';

    SetConsoleTextColor(7);

    cout << "Enter Window: "; // Window
    cin >> App;
    cout << "Enter Address (hex): "; // addres
    cin >> Adress;
    cout << "Enter Value: "; // Value
    cin >> Value;

    HWND hwnd = FindWindowA(0, App.c_str());
    if (hwnd == NULL) {
        SetConsoleTextColor(4);
        cout << "Window Not Found!" << endl;
        return 1;
    }

    DWORD pid;
    GetWindowThreadProcessId(hwnd, &pid);

    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (hProcess == NULL) {
        SetConsoleTextColor(4);
        cout << "Failed to open process!" << endl;
        return 1;
    }

    SetConsoleTextColor(2);
    cout << "Window Found, Process ID: " << pid << endl;

    uintptr_t addr;
    istringstream(Adress) >> hex >> addr;
    int val;
    istringstream(Value) >> val;

    int buffer;

    if (ReadProcessMemory(hProcess, (LPCVOID)addr, &buffer, sizeof(buffer), NULL)) {
        cout << "Current Value at Address: " << buffer << endl;
    }
    else {
        SetConsoleTextColor(4);
        cout << "Failed to read memory!" << endl;
    }

    if (WriteProcessMemory(hProcess, (LPVOID)addr, &val, sizeof(val), NULL)) {
        cout << "Value written successfully!" << endl;
    }
    else {
        SetConsoleTextColor(4);
        cout << "Failed to write memory!" << endl;
    }

    CloseHandle(hProcess);

    SetConsoleTextColor(7);
    return 0;
}