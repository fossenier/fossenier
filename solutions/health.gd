class_name Health

extends RefCounted

signal on_death

## An object used to model health, used for any object that has hit points
##
## Represents health as 2 variables: [member Health.health] and [member Health.max_health]
## Contains functionality to [method Health.damage], [method Health.heal], [method Health.is_dead], 
## [method Health.get_current_health], and [method Health.get_max_health]

## Current number of hit points remaining
var health:int
## Maximum number of hit points possible
var max_health:int

## Initializes new Health object with [member max_health] and [member health] both defaulting to 10.
func _init() -> void:
	max_health = 10
	health = 10
	
## Reduces [member health] by [param d] points. [member health] cannot go below 0
func damage(d:int) -> void:
	health = clamp(health - d, 0, max_health)
	if health == 0:
		on_death.emit()
	
## Increases [member health] by [param h] points. [member health] cannot go above [member max_health]
func heal(h:int) -> void:
	health = clamp(health + h, 0, max_health)
	
## Returns whether or not the object is dead (i.e., [member health] <= 0). [br]
## Returns [code]true[/code] if dead, [code]false[/code] if still alive.
func is_dead() -> bool:
	return health == 0

## Returns the current value of [member health].
func get_current_health() -> int:
	return health

## Returns the current value of [member max_health]
func get_max_health() -> int:
	return max_health
