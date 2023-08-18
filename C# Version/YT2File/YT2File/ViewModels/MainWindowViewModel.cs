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
public partial class MainWindowViewModel : ObservableObject
{

    // Starts when the viewmodel is initialized
    public MainWindowViewModel()
    {

    }
}
