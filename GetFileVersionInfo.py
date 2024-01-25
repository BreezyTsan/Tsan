def getFileVersionInfo(file_path):
    """
    Read all properties of the given file return them as a dictionary.
    :param self:
    :param file_path:
    :return: dict
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
                 'CompanyName', 'LegalCopyright', 'ProductVersion',
                 'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                 'FileVersion', 'OriginalFilename', 'SpecialBuild',)
    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}
    try:
        import win32api
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(file_path, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / fixedInfo['StrucVersion'],
                                                fixedInfo['FileVersionMS'] % fixedInfo['StrucVersion'],
                                                fixedInfo['FileVersionLS'] / fixedInfo['StrucVersion'],
                                                fixedInfo['FileVersionLS'] % fixedInfo['StrucVersion'])
        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(file_path, '\\VarFileInfo\\Translation')[0]
        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above
        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            # print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(file_path, strInfoPath)
        props['StringFileInfo'] = strInfo
    except Exception:
        pass
    if props["StringFileInfo"]:
        return props
    return None
