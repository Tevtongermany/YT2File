using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows.Controls;
using System.Windows.Markup;

namespace YT2File.View.Extensions;

public static class EnumExtensions
{
    public static string GetDescription(this Enum value)
    {
        return value.GetType().GetField(value.ToString())?.GetCustomAttributes(typeof(DescriptionAttribute), false).SingleOrDefault() is not DescriptionAttribute attribute ? value.ToString() : attribute.Description;
    }
}
public class EnumToItemsSource : MarkupExtension
{
    private readonly Type _type;

    public EnumToItemsSource(Type type)
    {
        _type = type;
    }

    public override object ProvideValue(IServiceProvider serviceProvider)
    {
        var values = Enum.GetValues(_type).Cast<Enum>();
        return values.Select(x => x.GetDescription()).ToList();
    }
}