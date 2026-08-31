using Godot;

public partial class Water : Node2D
{
    [Export] public float WaveParallaxFactor = 1.5f;
    [Export] public float DeepLayerParallaxFactor = 0.7f;

    private Sprite2D _deepLayer;
    private Sprite2D _waveLayer;
    private Node _driftController;

    public override void _Ready()
    {
        _deepLayer = GetNode<Sprite2D>("DeepLayer");
        _waveLayer = GetNode<Sprite2D>("WaveLayer");
        _driftController = GetTree().Root.GetNodeOrNull("Main/RandomDriftController");
    }

    public override void _Process(double delta)
    {
        if (_driftController is RandomDriftController drift)
        {
            // 视差：水往 raft 移动方向的反向滚动（让玩家"看到"漂流感）
            Vector2 driftVel = drift.CurrentVelocity;
            Vector2 deepOffset = -driftVel * DeepLayerParallaxFactor * (float)delta;
            Vector2 waveOffset = -driftVel * WaveParallaxFactor * (float)delta;
            _deepLayer.Position += deepOffset;
            _waveLayer.Position += waveOffset;
        }
    }
}
