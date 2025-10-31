extends GutTest

func test_constructor():
	var health:Health = Health.new()
	assert_eq(health.get_current_health(), 10)
	assert_eq(health.get_max_health(), 10)
	assert_false(health.is_dead())
	
func test_damage():
	var health:Health = Health.new()
	
	health.damage(1)
	assert_eq(health.get_current_health(), 9)
	assert_false(health.is_dead())
	
	health.damage(5)
	assert_eq(health.get_current_health(), 4)
	assert_false(health.is_dead())
	
	health.damage(4)
	assert_eq(health.get_current_health(), 0)
	assert_true(health.is_dead())
	
	health.damage(1)
	assert_eq(health.get_current_health(), 0)
	assert_true(health.is_dead())
	
func test_heal():
	var health:Health = Health.new()
	
	health.heal(5)
	assert_eq(health.get_current_health(), 10)
	assert_false(health.is_dead())
	
	health.damage(5)
	health.heal(2)
	assert_eq(health.get_current_health(), 7)
	assert_false(health.is_dead())
	
	health.heal(4)
	assert_eq(health.get_current_health(), 10)
	assert_false(health.is_dead())
