import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bmi_core import (
    calculate_bmi,
    bmi_category,
    calculate_bmr_mifflin,
    healthy_weight_range_for_height,
    recommended_water_liters_per_day,
    lb_to_kg,
    cms_to_meters,
    bmi_report
)


# ==================== Unit Conversion Tests ====================

class TestUnitConversions:
    def test_lb_to_kg(self):
        assert lb_to_kg(220) == pytest.approx(99.79, rel=0.01)
        assert lb_to_kg(0) == 0
        assert lb_to_kg(100) == pytest.approx(45.36, rel=0.01)

    def test_cms_to_meters(self):
        assert cms_to_meters(175) == pytest.approx(1.75, rel=0.01)
        assert cms_to_meters(100) == 1.0
        assert cms_to_meters(0) == 0


# ==================== BMI Calculation Tests ====================

class TestCalculateBMI:
    def test_normal_bmi(self):
        # 70kg, 1.75m -> BMI = 22.86
        bmi = calculate_bmi(70, 1.75)
        assert bmi == pytest.approx(22.86, rel=0.01)

    def test_underweight_bmi(self):
        # 50kg, 1.75m -> BMI = 16.33
        bmi = calculate_bmi(50, 1.75)
        assert bmi == pytest.approx(16.33, rel=0.01)

    def test_overweight_bmi(self):
        # 85kg, 1.75m -> BMI = 27.76
        bmi = calculate_bmi(85, 1.75)
        assert bmi == pytest.approx(27.76, rel=0.01)

    def test_obese_bmi(self):
        # 100kg, 1.75m -> BMI = 32.65
        bmi = calculate_bmi(100, 1.75)
        assert bmi == pytest.approx(32.65, rel=0.01)

    def test_zero_height_raises_error(self):
        with pytest.raises((ZeroDivisionError, ValueError)):
            calculate_bmi(70, 0)

    def test_negative_weight_raises_error(self):
        with pytest.raises(ValueError):
            calculate_bmi(-70, 1.75)

    def test_negative_height_raises_error(self):
        with pytest.raises(ValueError):
            calculate_bmi(70, -1.75)


# ==================== BMI Category Tests ====================

class TestBMICategory:
    def test_underweight(self):
        category, description = bmi_category(17.5)
        assert "underweight" in category.lower()

    def test_normal_weight(self):
        category, description = bmi_category(22.0)
        assert "normal" in category.lower()

    def test_overweight(self):
        category, description = bmi_category(27.0)
        assert "overweight" in category.lower()

    def test_obesity_class_1(self):
        category, description = bmi_category(32.0)
        assert "obesity" in category.lower() or "obese" in category.lower()

    def test_obesity_class_2(self):
        category, description = bmi_category(37.0)
        assert "obesity" in category.lower() or "obese" in category.lower()

    def test_obesity_class_3(self):
        category, description = bmi_category(42.0)
        assert "obesity" in category.lower() or "obese" in category.lower()

    def test_boundary_underweight_normal(self):
        # 18.5 is the boundary
        assert "normal" in bmi_category(18.5)[0].lower()
        assert "underweight" in bmi_category(18.4)[0].lower()

    def test_boundary_normal_overweight(self):
        # 25 is the boundary
        assert "overweight" in bmi_category(25.0)[0].lower()
        assert "normal" in bmi_category(24.9)[0].lower()

    def test_boundary_overweight_obese(self):
        # 30 is the boundary
        assert "obesity" in bmi_category(30.0)[0].lower() or "obese" in bmi_category(30.0)[0].lower()
        assert "overweight" in bmi_category(29.9)[0].lower()


# ==================== BMR Calculation Tests ====================

class TestCalculateBMR:
    def test_bmr_male(self):
        # Mifflin-St Jeor for male: (10 * 70) + (6.25 * 175) - (5 * 25) + 5 = 1673.75
        bmr = calculate_bmr_mifflin(70, 175, 25, 'male')
        assert bmr == pytest.approx(1673.75, rel=0.01)

    def test_bmr_female(self):
        # Mifflin-St Jeor for female: (10 * 60) + (6.25 * 165) - (5 * 25) - 161 = 1345.25
        bmr = calculate_bmr_mifflin(60, 165, 25, 'female')
        assert bmr == pytest.approx(1345.25, rel=0.01)

    def test_bmr_increases_with_weight(self):
        bmr_light = calculate_bmr_mifflin(60, 175, 25, 'male')
        bmr_heavy = calculate_bmr_mifflin(80, 175, 25, 'male')
        assert bmr_heavy > bmr_light

    def test_bmr_decreases_with_age(self):
        bmr_young = calculate_bmr_mifflin(70, 175, 25, 'male')
        bmr_old = calculate_bmr_mifflin(70, 175, 50, 'male')
        assert bmr_young > bmr_old

    def test_bmr_male_higher_than_female(self):
        bmr_male = calculate_bmr_mifflin(70, 175, 25, 'male')
        bmr_female = calculate_bmr_mifflin(70, 175, 25, 'female')
        assert bmr_male > bmr_female


# ==================== Healthy Weight Range Tests ====================

class TestHealthyWeightRange:
    def test_healthy_range_175cm(self):
        # For 1.75m: 18.5 * 1.75^2 = 56.66, 24.9 * 1.75^2 = 76.27
        low, high = healthy_weight_range_for_height(1.75)
        assert low == pytest.approx(56.66, rel=0.02)
        assert high == pytest.approx(76.27, rel=0.02)

    def test_healthy_range_increases_with_height(self):
        low_short, high_short = healthy_weight_range_for_height(1.60)
        low_tall, high_tall = healthy_weight_range_for_height(1.80)
        assert low_tall > low_short
        assert high_tall > high_short

    def test_healthy_range_returns_tuple(self):
        result = healthy_weight_range_for_height(1.75)
        assert isinstance(result, tuple)
        assert len(result) == 2


# ==================== Water Intake Tests ====================

class TestWaterIntake:
    def test_water_intake_70kg(self):
        # General formula: weight * 0.033 = 2.31 liters
        water = recommended_water_liters_per_day(70)
        assert water == pytest.approx(2.31, rel=0.1)

    def test_water_intake_increases_with_weight(self):
        water_light = recommended_water_liters_per_day(50)
        water_heavy = recommended_water_liters_per_day(100)
        assert water_heavy > water_light

    def test_water_intake_positive(self):
        water = recommended_water_liters_per_day(70)
        assert water > 0


# ==================== BMI Report Integration Tests ====================

class TestBMIReport:
    def test_report_returns_all_values(self):
        result = bmi_report(
            weight=70,
            height=1.75,
            age=25,
            sex='male',
            weight_unit='kg',
            height_unit='m'
        )
        assert result is not None
        assert len(result) >= 6  # At least BMI, category, description, BMR, healthy_range, water

    def test_report_with_metric_units(self):
        result = bmi_report(
            weight=70,
            height=1.75,
            age=25,
            sex='male',
            weight_unit='kg',
            height_unit='m'
        )
        bmi = result[0]
        assert bmi == pytest.approx(22.86, rel=0.01)

    def test_report_with_imperial_weight(self):
        result = bmi_report(
            weight=154,  # ~70kg
            height=1.75,
            age=25,
            sex='male',
            weight_unit='lb',
            height_unit='m'
        )
        bmi = result[0]
        assert bmi == pytest.approx(22.86, rel=0.1)

    def test_report_with_cm_height(self):
        result = bmi_report(
            weight=70,
            height=175,
            age=25,
            sex='male',
            weight_unit='kg',
            height_unit='cm'
        )
        bmi = result[0]
        assert bmi == pytest.approx(22.86, rel=0.01)


# ==================== Edge Cases ====================

class TestEdgeCases:
    def test_very_low_bmi(self):
        category, description = bmi_category(10.0)
        assert "underweight" in category.lower()

    def test_very_high_bmi(self):
        category, description = bmi_category(50.0)
        assert "obesity" in category.lower() or "obese" in category.lower()

    def test_exact_boundary_values(self):
        # Test exact WHO boundaries
        assert "underweight" in bmi_category(18.49)[0].lower()
        assert "normal" in bmi_category(18.50)[0].lower()
        assert "normal" in bmi_category(24.99)[0].lower()
        assert "overweight" in bmi_category(25.00)[0].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])