using System;
using CommunityToolkit.Mvvm.ComponentModel;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Reflection;
using YT2File.Enums;
using YT2File.Helper;
using System.IO.Compression;
using YT2File.View;
using System.Windows;

namespace YT2File.ViewModels;

public partial class SplashScreenViewModel : ObservableObject
{
    private string _title = string.Empty;
    private readonly Window _window;
    public string Title
    {
        get { return _title; }
        set
        {
            _title = value;
            OnPropertyChanged(nameof(Title));
        }
    }
    public SplashScreenViewModel(Window window)
    {
        Title = "Starting Check";
        _window = window;
    }
    public async Task check()
    {
        
        if (Directory.Exists("Deps"))
        {
            Title = "Directory Exists!";
        }
        else
        {
            Title = "Directory Doesn't Exists. Making one";
            Directory.CreateDirectory("Deps");

        }
        Title = "Checking If YT-DLP is Installed";
        if (File.Exists("Deps/yt-dlp.exe"))
        {
            Title = "YT-DLP is Installed!";
        }
        else
        {
            Title = "YT-DLP is not installed Downloading it!";
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    HttpResponseMessage response = await client.GetAsync("https://github.com/yt-dlp/yt-dlp/releases/download/2023.03.04/yt-dlp.exe");
                    response.EnsureSuccessStatusCode();

                    using (HttpContent content = response.Content)
                    {
                        await using (var stream = await content.ReadAsStreamAsync())
                        {
                            using (var fileStream = new FileStream("Deps/yt-dlp.exe", FileMode.Create, FileAccess.Write))
                            {
                                await stream.CopyToAsync(fileStream);
                            }
                        }
                    }
                }

                Title = "Downloading YT-DLP Done";
            }
            catch (Exception ex)
            {
                Title = "Error " + ex.Message;
                await Task.Delay(5000);
                System.Windows.Application.Current.Shutdown();
            }
        }
        Title = "Checking If FFmpeg is installed";
        if (Directory.Exists("Deps/ffmpeg/bin"))
        {
            Title = "FFmpeg is installed!";
        }
        else if (File.Exists("Deps/ffmpeg-master-latest-win64-gpl.zip"))
        {
            Title = "FFmpeg Already Downloaded, Unzipping it";
            ZipFile.ExtractToDirectory("Deps/ffmpeg-master-latest-win64-gpl.zip", "Deps");
            Directory.Move("Deps/ffmpeg-master-latest-win64-gpl", "Deps/ffmpeg");

        }
        else
        {
            Title = "FFmpeg is not installed Downloading it, Might take a while";
            try
            {
                using (HttpClient client = new HttpClient())
                {
                    HttpResponseMessage response = await client.GetAsync("https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip");
                    response.EnsureSuccessStatusCode();

                    using (HttpContent content = response.Content)
                    {
                        await using (var stream = await content.ReadAsStreamAsync())
                        {
                            using (var fileStream = new FileStream("Deps/ffmpeg-master-latest-win64-gpl.zip", FileMode.Create, FileAccess.Write))
                            {
                                await stream.CopyToAsync(fileStream);
                                Title = "Downloading FFmpeg Done";
                            }
                        }
                    }
                }

                
                await Task.Delay(2000);
                Title = "Unzipping FFmpeg";
                ZipFile.ExtractToDirectory("Deps/ffmpeg-master-latest-win64-gpl.zip", "Deps");
                Directory.Move("Deps/ffmpeg-master-latest-win64-gpl", "Deps/ffmpeg");
                Title = "Done!";
            }
            catch (Exception ex)
            {
                Title = "Error " + ex.Message;
                await Task.Delay(5000);
                Application.Current.Shutdown();
            }
        }
        MainWindow mainWindow = new MainWindow();
        mainWindow.Show();
        _window.Close();
        

    }



}
