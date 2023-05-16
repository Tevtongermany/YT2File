using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace YT2File.Enums;

public enum EFormat
{
    [Description("MP4")]
    video,
    [Description("MP3")]
    audio
}