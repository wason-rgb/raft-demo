using Godot;

public partial class Debris : Node2D
{
    [Export] public float WrapMargin = 100.0f;
    [Export] public float MinRespawnSeconds = 4.0f;
    [Export] public float MaxRespawnSeconds = 12.0f;
    [Export] public float YMin = 400.0f;
    [Export] public float YMax = 700.0f;

    private float _x;
    private float _y;
    private float _respawnTimer = 0.0f;
    private RandomNumberGenerator _rng = new RandomNumberGenerator();

    public override void _Ready()
    {
        _rng.Randomize();
        _y = _rng.RandfRange(YMin, YMax);
        Respawn();
    }

    public override void _Process(double delta)
    {
        _respawnTimer += (float)delta;
        var driftController = GetTree().Root.GetNodeOrNull("Main/RandomDriftController");
        if (driftController is RandomDriftController drift)
        {
            _x += -drift.CurrentVelocity.X * (float)delta * 1.5f;
            Position = new Vector2(_x, _y);
            if (_x < -WrapMargin || _respawnTimer > MaxRespawnSeconds)
            {
                Respawn();
            }
        }
    }

    private void Respawn()
    {
        _x = 1920 + WrapMargin + _rng.RandfRange(0, 200);
        _y = _rng.RandfRange(YMin, YMax);
        _respawnTimer = 0.0f;
    }
}
