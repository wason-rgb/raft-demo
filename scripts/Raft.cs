using Godot;

public partial class Raft : Node2D
{
    [Export] public float BobAmplitude = 4.0f;
    [Export] public float BobPeriodSeconds = 2.4f;
    [Export] public Vector2 ScreenCenter = new Vector2(960, 540);

    private float _elapsed = 0.0f;

    public override void _Ready()
    {
        Position = ScreenCenter;
    }

    public override void _Process(double delta)
    {
        _elapsed += (float)delta;
        // 上下呼吸：sin 波
        float bobOffset = Mathf.Sin(_elapsed * Mathf.Tau / BobPeriodSeconds) * BobAmplitude;
        Position = new Vector2(ScreenCenter.X, ScreenCenter.Y + bobOffset);
    }
}
