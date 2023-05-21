using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using YT2File;
using YT2File.Enums;
using YT2File.Helper;
using System.Threading;
using System.Net.Http;
using Serilog;
using System.Diagnostics;

namespace YT2File.ViewModels;

public partial class MainWindowViewModel : ObservableObject
{
    // Command Stuff
    public ICommand TestCommand { get; }
    public ICommand StartDownloadCommand { get; }

    // Starts when the viewmodel is initialized
    public MainWindowViewModel()
    {
        TestCommand = new RelayCommand(test);
        StartDownloadCommand = new RelayCommand(Download);
        
    }
    // Variables
    public string lastURL { get; set; } = string.Empty;
    public EFormat Format
    {
        get => AppSettings.Current.Format;
        set
        {
            AppSettings.Current.Format = value;
            AppSettings.Save();
            OnPropertyChanged();
        }
    }

    // Functions
    [RelayCommand]
    public static void test()
    {
        Console.WriteLine("test");
    }

    [RelayCommand]
    public void Download()
    {
        Thread t = new Thread(new ThreadStart(StartDownload));
        t.Start();
    }
    public void StartDownload()
    {
        switch (Format)
        {
            case 0:
                try
                {
                    ProcessStartInfo startInfo = new ProcessStartInfo();
                    startInfo.FileName = "Deps/yt-dlp.exe";
                    startInfo.Arguments = $"-f mp4 --ffmpeg-location Deps/ffmpeg/bin {lastURL}";
                    startInfo.WindowStyle = ProcessWindowStyle.Hidden;

                    using (Process process = new Process())
                    {
                        process.StartInfo = startInfo;
                        process.Start();
                        process.WaitForExit();
                    }

                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error: " + ex.Message);
                }
                break;
            case (EFormat)1:
                try
                {
                    ProcessStartInfo startInfo = new ProcessStartInfo();
                    startInfo.FileName = "Deps/yt-dlp.exe";
                    startInfo.Arguments = $"--extract-audio --audio-format mp3 --ffmpeg-location Deps/ffmpeg/bin {lastURL}";
                    startInfo.WindowStyle = ProcessWindowStyle.Hidden;

                    using (Process process = new Process())
                    {
                        process.StartInfo = startInfo;
                        process.Start();
                        process.WaitForExit();
                    }

                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error: " + ex.Message);
                }
                break;
        }

    }

}
