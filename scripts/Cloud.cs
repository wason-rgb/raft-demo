using Godot;

public partial class Cloud : Node2D
{
    [Export] public float WrapMargin = 200.0f;
    [Export] public Vector2 StartPosition = new Vector2(400, 200);

    private float _x;

    public override void _Ready()
    {
        _x = StartPosition.X;
    }

    public override void _Process(double delta)
    {
        var driftController = GetTree().Root.GetNodeOrNull("Main/RandomDriftController");
        if (driftController is RandomDriftController drift)
        {
            _x += -drift.CurrentVelocity.X * (float)delta * 0.5f;
            // 出屏回卷
            if (_x < -WrapMargin) _x = 1920 + WrapMargin;
            else if (_x > 1920 + WrapMargin) _x = -WrapMargin;
            Position = new Vector2(_x, StartPosition.Y);
        }
    }
}
