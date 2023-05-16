using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using YT2File.Helper;

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
    }

}
