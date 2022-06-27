#ifndef __UTILS__
#define __UTILS__

#include <string>
#include <vector>

using namespace std;

class Utils
{
public:
    static bool isNumber(const string &str);

    template <typename T>
    static bool allEqual(vector<T> const &v)
    {
        return adjacent_find(v.begin(), v.end(), not_equal_to<T>()) == v.end();
    }

};

#endif