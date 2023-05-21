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
using System.Windows.Shapes;
using YT2File.ViewModels;

namespace YT2File.View
{
    /// <summary>
    /// Interaction logic for SplashScreen.xaml
    /// </summary>
    public partial class SplashScreen
    {
        public SplashScreen()
        {
            InitializeComponent();
            AppVM.SplashScreenVM = new SplashScreenViewModel(this);
            DataContext = AppVM.SplashScreenVM;
        }
        private async void OnLoaded(object sender, RoutedEventArgs e)
        {
            await AppVM.SplashScreenVM.check();
        }
    }

}
