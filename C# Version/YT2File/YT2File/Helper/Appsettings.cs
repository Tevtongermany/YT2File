using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Xml;
using CommunityToolkit.Mvvm.ComponentModel;
using YT2File.Enums;
using Newtonsoft.Json;

namespace YT2File.Helper;

public partial class AppSettings : ObservableObject
{
    public static AppSettings Current;

    public static readonly DirectoryInfo DirectoryPath = new(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "YT2File"));
    public static readonly DirectoryInfo FilePath = new(Path.Combine(DirectoryPath.FullName, "AppSettings.json"));

    public static void Load()
    {
        if (File.Exists(FilePath.FullName))
        {
            Current = JsonConvert.DeserializeObject<AppSettings>(File.ReadAllText(FilePath.FullName));
        }

        Current ??= new AppSettings();
    }

    public static void Save()
    {
        File.WriteAllText(FilePath.FullName, JsonConvert.SerializeObject(Current, Newtonsoft.Json.Formatting.Indented));
    }

    [ObservableProperty] private EFormat format = EFormat.video;
    [ObservableProperty] private string downloadpath = "";

   
}
// Shout out to half check him out here since everything in this file was made by him and not me
// i hope it isn't bad that im using his code
// https://github.com/halfuwu/