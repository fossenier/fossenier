class_name Player

extends CharacterBody2D

var health:Health

@export var speed:float = 300

func _ready() -> void:
	health = Health.new()
	health.on_death.connect(die)
	update_health_ui()

func _process(delta: float) -> void:
	var input_direction:Vector2 = Input.get_vector("Left", "Right", "Up", "Down")
	velocity = input_direction * speed
	move_and_slide()

func receive_damage(d:float) -> void:
	health.damage(d)
	if health.is_dead():
		print("player dead. Game Over.")
	update_health_ui()

func receive_heal(h:float) -> void:
	health.heal(h)
	update_health_ui()

func die():
	print("Player dead")

func update_health_ui():
	$HealthLabel.text = str(health.get_current_health()) + " / " + str(health.get_max_health())
