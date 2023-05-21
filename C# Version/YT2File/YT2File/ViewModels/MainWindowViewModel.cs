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
using System.Text.Json;
using System.Security.Policy;

namespace YT2File.ViewModels;
class YTData
{
    public List<VideoItem> Items { get; set; }
}
class VideoItem
{
    public Snippet Snippet { get; set; }
}
class Snippet
{
    public string Title { get; set; }
    public string Description { get; set; }
}
public partial class MainWindowViewModel : ObservableObject
{
    // Command Stuff
    public ICommand TestCommand { get; }
    public IAsyncRelayCommand DownloadCommand { get; }

    // Starts when the viewmodel is initialized
    public MainWindowViewModel()
    {
        TestCommand = new RelayCommand(test);
        DownloadCommand = new AsyncRelayCommand(StartDownload);
        
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
    private string _yttitle = string.Empty;
    public string YTTitle
    {
        get { return _yttitle; }
        set
        {
            _yttitle = value;
            OnPropertyChanged(nameof(YTTitle));
        }
    }

    // Functions
    [RelayCommand]
    public static void test()
    {
        Console.WriteLine("test");
    }

    [RelayCommand]

    public async Task StartDownload()
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

    private async Task GetMetaData(string Url)
    {
        using (HttpClient client = new HttpClient())
        {
            try
            {
                HttpResponseMessage response = await client.GetAsync(Url);
                response.EnsureSuccessStatusCode(); // Throw an exception if the response is not successful

                string jsonResponse = await response.Content.ReadAsStringAsync();

                // Deserialize the JSON into an object
                var data = JsonSerializer.Deserialize<YTData>(jsonResponse);

                // Access the properties of the data object
                YTTitle = data.Items[0].Snippet.Title;
                // ...

            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine("Error: " + ex.Message);
            }
        }
    }
}