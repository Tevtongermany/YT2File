using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace YT2File.ViewModel
{
    internal partial class MainWindowViewModel : ObservableObject
    {
        public ICommand TestCommand { get; }

        public MainWindowViewModel()
        {
            TestCommand = new RelayCommand(test);
        }
        

        [RelayCommand]
        public static void test()
        {
            Console.WriteLine("test");
        }

    }



}
