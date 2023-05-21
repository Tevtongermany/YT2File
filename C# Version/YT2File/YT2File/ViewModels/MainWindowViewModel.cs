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
        
        // Creates logger
        initialize();
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
                Console.WriteLine("Video Download Thread started ");
                break;
            case (EFormat)1:
                Console.WriteLine("Thread Stgarted");
                break;
        }

    }
    public void initialize()
    {

        Console.WriteLine("Checking if YT DLP Exists");
        if (File.Exists("yt-dlp.exe"))
        {
            Console.WriteLine("youtube_dlp exists Checking if FFmpeg is Installed");

            if (File.Exists("ffmpeg/bin"))
            {
                Console.WriteLine("FFmpeg is Installed done Checking");
            }
        }
        else
        {
            Console.WriteLine("youtube_dlp Doesn't Exist ");
        }
    }

}
