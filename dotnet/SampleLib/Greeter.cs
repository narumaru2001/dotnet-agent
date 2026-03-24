namespace SampleLib;

public class Greeter
{
    public string Hello(string name)
        => $"Hello, {name}!";

    public string Greet(string name, string language)
        => language switch
        {
            "ja" => $"こんにちは、{name}さん！",
            "en" => $"Hello, {name}!",
            "fr" => $"Bonjour, {name}!",
            _ => $"Hi, {name}!"
        };
}
