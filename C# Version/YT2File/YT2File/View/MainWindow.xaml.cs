using System.Runtime.InteropServices;
using YT2File.Services;
using YT2File.Helper;
using YT2File.ViewModels;
using System.Globalization;
using System.Windows.Data;
using System;
using YT2File.View.Extensions;
using System.Linq;

namespace YT2File.View;

public partial class MainWindow
{
    [DllImport("kernel32")]
    private static extern bool AllocConsole();

    [DllImport("kernel32")]
    private static extern bool FreeConsole();
    public MainWindow()
    {
        InitializeComponent();
        AllocConsole();
        AppSettings.DirectoryPath.Create();
        AppSettings.Load();
        AppVM.MainVM = new MainWindowViewModel();
        DataContext = AppVM.MainVM;

    }
    //  Enum to String
    public class EnumToStringConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            var enumValue = (Enum)value;
            return enumValue.GetDescription();
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            var values = Enum.GetValues(targetType).Cast<Enum>();
            return values.FirstOrDefault(x => x.GetDescription().Equals(value)) ?? value;
        }
    }
    
}
