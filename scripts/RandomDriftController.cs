using Godot;
using System;

public partial class RandomDriftController : Node2D
{
    // 漂移配置
    [Export] public float MinSpeed = 80.0f;
    [Export] public float MaxSpeed = 120.0f;
    [Export] public float MinDirectionDuration = 5.0f;
    [Export] public float MaxDirectionDuration = 15.0f;
    [Export] public float DirectionChangeSmoothingMs = 100.0f;

    public Vector2 CurrentDirection { get; private set; } = Vector2.Right;
    public float CurrentSpeed { get; private set; } = 100.0f;
    public Vector2 CurrentVelocity => CurrentDirection * CurrentSpeed;

    private float _directionTimer = 0.0f;
    private float _currentDirectionDuration = 0.0f;
    private Vector2 _targetDirection = Vector2.Right;
    private float _targetSpeed = 100.0f;
    private float _smoothingTimeMs = 0.0f;
    private Random _rng = new Random();

    public override void _Ready()
    {
        PickNewTarget();
        _currentDirectionDuration = (float)(MinDirectionDuration + _rng.NextDouble() * (MaxDirectionDuration - MinDirectionDuration));
    }

    public override void _Process(double delta)
    {
        // 累计方向持续时间
        _directionTimer += (float)delta;
        if (_directionTimer >= _currentDirectionDuration)
        {
            PickNewTarget();
            _directionTimer = 0.0f;
            _currentDirectionDuration = (float)(MinDirectionDuration + _rng.NextDouble() * (MaxDirectionDuration - MinDirectionDuration));
        }

        // 平滑切换方向
        if (CurrentDirection != _targetDirection)
        {
            _smoothingTimeMs += (float)(delta * 1000.0);
            float t = Mathf.Clamp(_smoothingTimeMs / DirectionChangeSmoothingMs, 0.0f, 1.0f);
            CurrentDirection = CurrentDirection.Lerp(_targetDirection, t).Normalized();
            if (CurrentDirection.DistanceTo(_targetDirection) < 0.01f)
            {
                CurrentDirection = _targetDirection;
                _smoothingTimeMs = 0.0f;
            }
        }

        // 平滑切换速度
        CurrentSpeed = Mathf.Lerp(CurrentSpeed, _targetSpeed, (float)delta * 2.0f);
    }

    private void PickNewTarget()
    {
        // 随机选 0-360 度方向
        float angleDegrees = (float)(_rng.NextDouble() * 360.0);
        _targetDirection = Vector2.Right.Rotated(Mathf.DegToRad(angleDegrees));
        _targetSpeed = (float)(MinSpeed + _rng.NextDouble() * (MaxSpeed - MinSpeed));
        _smoothingTimeMs = 0.0f;
    }
}
