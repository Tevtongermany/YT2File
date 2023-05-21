using System.Windows;
using AdonisUI.Controls;
using CommunityToolkit.Mvvm.ComponentModel;
using YT2File.Helper;
using YT2File.ViewModels;
using YT2File.View;
using YT2File;
using MessageBox = AdonisUI.Controls.MessageBox;
using MessageBoxImage = AdonisUI.Controls.MessageBoxImage;

namespace YT2File.ViewModels;

public class ApplicationViewModel : ObservableObject
{
    public MainWindowViewModel MainVM;

    public void Warning(string caption, string message)
    {
        Application.Current.Dispatcher.Invoke(() =>
        {
            var messageBox = new MessageBoxModel
            {
                Caption = caption,
                Icon = MessageBoxImage.Warning,
                Text = message,
                Buttons = new[] { MessageBoxButtons.Ok() }
            };

            //AppLog.Warning($"{caption}: {message}");
            MessageBox.Show(messageBox);
        });
    }


    public void Quit()
    {
        AppSettings.Save();
        Application.Current.Shutdown();
    }
}