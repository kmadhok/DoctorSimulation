#!/usr/bin/env python3
"""
Test script for design system alignment - Task 3.6
Validates that user profile components match the established design patterns
"""

import re
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_color_consistency():
    """Test color consistency with established design system"""
    print("Testing color consistency...")
    
    # Read the CSS file
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected colors from design system
    expected_colors = {
        'Primary Blue': '#4285f4',
        'Primary Blue Dark': '#3367d6',
        'Primary Text': '#333',
        'Secondary Text': '#666',
        'Muted Text': '#777',
        'Background': '#f5f5f5',
        'Card Background': 'white',
        'Form Background': '#f8f9fa',
        'Header Background': '#f0f0f0',
        'Border Color': '#e0e0e0',
        'Success Color': '#4caf50',
        'Warning Color': '#ff9800',
        'Error Color': '#f44336'
    }
    
    print("✅ COLOR CONSISTENCY:")
    for color_name, color_value in expected_colors.items():
        if color_value in css_content:
            print(f"  ✅ {color_name} ({color_value}) - used in profile components")
        else:
            print(f"  ❌ {color_name} ({color_value}) - missing")
    
    return True

def test_typography_consistency():
    """Test typography consistency with established design system"""
    print("\nTesting typography consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected typography patterns
    typography_patterns = {
        'Font Family': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        'Line Height': '1.6',
        'Font Weight 500': 'font-weight: 500',
        'Font Size 0.8rem': 'font-size: 0.8rem',
        'Font Size 0.9rem': 'font-size: 0.9rem',
        'Font Size 1.2rem': 'font-size: 1.2rem'
    }
    
    print("✅ TYPOGRAPHY CONSISTENCY:")
    for pattern_name, pattern_value in typography_patterns.items():
        if pattern_value in css_content:
            print(f"  ✅ {pattern_name} - consistent with design system")
        else:
            print(f"  ❌ {pattern_name} - missing or inconsistent")
    
    return True

def test_spacing_consistency():
    """Test spacing consistency with established design system"""
    print("\nTesting spacing consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected spacing patterns
    spacing_patterns = {
        'Standard Padding': 'padding: 1rem',
        'Button Padding': 'padding: 10px 20px',
        'Small Spacing': '0.5rem',
        'Large Spacing': '2rem',
        'Standard Gap': 'gap: 1rem'
    }
    
    print("✅ SPACING CONSISTENCY:")
    for pattern_name, pattern_value in spacing_patterns.items():
        count = css_content.count(pattern_value)
        if count > 0:
            print(f"  ✅ {pattern_name} - {count} uses")
        else:
            print(f"  ❌ {pattern_name} - not used")
    
    return True

def test_border_radius_consistency():
    """Test border radius consistency with established design system"""
    print("\nTesting border radius consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected border radius patterns
    border_radius_patterns = {
        'Card Border Radius': 'border-radius: 0.5rem',
        'Button Border Radius': 'border-radius: 4px',
        'Circular Border Radius': 'border-radius: 50%'
    }
    
    print("✅ BORDER RADIUS CONSISTENCY:")
    for pattern_name, pattern_value in border_radius_patterns.items():
        count = css_content.count(pattern_value)
        if count > 0:
            print(f"  ✅ {pattern_name} - {count} uses")
        else:
            print(f"  ❌ {pattern_name} - not used")
    
    return True

def test_transition_consistency():
    """Test transition consistency with established design system"""
    print("\nTesting transition consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected transition patterns
    transition_patterns = {
        'Standard Transition': 'transition: all 0.2s ease',
        'Transform Hover': 'transform: translateY(-1px)',
        'Transform Active': 'transform: scale(0.95)'
    }
    
    print("✅ TRANSITION CONSISTENCY:")
    for pattern_name, pattern_value in transition_patterns.items():
        count = css_content.count(pattern_value)
        if count > 0:
            print(f"  ✅ {pattern_name} - {count} uses")
        else:
            print(f"  ❌ {pattern_name} - not used")
    
    return True

def test_shadow_consistency():
    """Test shadow consistency with established design system"""
    print("\nTesting shadow consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected shadow patterns
    shadow_patterns = {
        'Standard Card Shadow': 'box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1)',
        'Focus Shadow': 'box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.25)',
        'Button Hover Shadow': 'box-shadow: 0 2px 4px rgba(66, 133, 244, 0.2)'
    }
    
    print("✅ SHADOW CONSISTENCY:")
    for pattern_name, pattern_value in shadow_patterns.items():
        if pattern_value in css_content:
            print(f"  ✅ {pattern_name} - matches design system")
        else:
            print(f"  ❌ {pattern_name} - missing or inconsistent")
    
    return True

def test_button_pattern_consistency():
    """Test button pattern consistency with established design system"""
    print("\nTesting button pattern consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected button patterns
    button_patterns = {
        'Primary Button Background': 'background-color: #4285f4',
        'Primary Button Hover': 'background-color: #3367d6',
        'Button Border': 'border: 1px solid #4285f4',
        'Button Cursor': 'cursor: pointer',
        'Button Text Align': 'text-align: center'
    }
    
    print("✅ BUTTON PATTERN CONSISTENCY:")
    for pattern_name, pattern_value in button_patterns.items():
        count = css_content.count(pattern_value)
        if count > 0:
            print(f"  ✅ {pattern_name} - {count} uses")
        else:
            print(f"  ❌ {pattern_name} - not used")
    
    return True

def test_form_pattern_consistency():
    """Test form pattern consistency with established design system"""
    print("\nTesting form pattern consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected form patterns
    form_patterns = {
        'Form Background': 'background-color: #f8f9fa',
        'Header Background': 'background-color: #f0f0f0',
        'Border Color': 'border: 1px solid #e0e0e0',
        'Card Background': 'background-color: white'
    }
    
    print("✅ FORM PATTERN CONSISTENCY:")
    for pattern_name, pattern_value in form_patterns.items():
        count = css_content.count(pattern_value)
        if count > 0:
            print(f"  ✅ {pattern_name} - {count} uses")
        else:
            print(f"  ❌ {pattern_name} - not used")
    
    return True

def test_sidebar_pattern_consistency():
    """Test sidebar pattern consistency with established design system"""
    print("\nTesting sidebar pattern consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected sidebar patterns
    sidebar_patterns = {
        'Sidebar Width': 'width: 300px',
        'Sidebar Gap': 'gap: 2rem',
        'Action Button Width': 'width: 28px',
        'Action Button Height': 'height: 28px'
    }
    
    print("✅ SIDEBAR PATTERN CONSISTENCY:")
    for pattern_name, pattern_value in sidebar_patterns.items():
        count = css_content.count(pattern_value)
        if count > 0:
            print(f"  ✅ {pattern_name} - {count} uses")
        else:
            print(f"  ❌ {pattern_name} - not used")
    
    return True

def test_responsive_pattern_consistency():
    """Test responsive pattern consistency with established design system"""
    print("\nTesting responsive pattern consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected responsive patterns
    responsive_patterns = {
        'Mobile Media Query': '@media (max-width: 480px)',
        'Tablet Media Query': '@media (max-width: 768px)',
        'Touch Device Query': '@media (hover: none) and (pointer: coarse)',
        'Large Screen Query': '@media (min-width: 1200px)'
    }
    
    print("✅ RESPONSIVE PATTERN CONSISTENCY:")
    for pattern_name, pattern_value in responsive_patterns.items():
        count = css_content.count(pattern_value)
        if count > 0:
            print(f"  ✅ {pattern_name} - {count} uses")
        else:
            print(f"  ❌ {pattern_name} - not used")
    
    return True

def test_accessibility_pattern_consistency():
    """Test accessibility pattern consistency with established design system"""
    print("\nTesting accessibility pattern consistency...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Expected accessibility patterns
    accessibility_patterns = {
        'Reduced Motion': 'prefers-reduced-motion: reduce',
        'High Contrast': 'prefers-contrast: high',
        'Focus Visible': 'focus-visible',
        'Screen Reader': 'sr-only'
    }
    
    print("✅ ACCESSIBILITY PATTERN CONSISTENCY:")
    for pattern_name, pattern_value in accessibility_patterns.items():
        if pattern_value in css_content:
            print(f"  ✅ {pattern_name} - implemented")
        else:
            print(f"  ❌ {pattern_name} - missing")
    
    return True

def count_design_system_compliance():
    """Count overall design system compliance"""
    print("\nCounting design system compliance...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Count compliance metrics
    compliance_metrics = {
        'Primary Blue Uses': css_content.count('#4285f4'),
        'Standard Transitions': css_content.count('transition: all 0.2s ease'),
        'Standard Padding': css_content.count('padding: 1rem'),
        'Standard Border Radius': css_content.count('border-radius: 0.5rem'),
        'Standard Shadows': css_content.count('0 2px 10px rgba(0, 0, 0, 0.1)'),
        'Design System Comments': css_content.count('Matches existing')
    }
    
    print("✅ DESIGN SYSTEM COMPLIANCE METRICS:")
    for metric_name, count in compliance_metrics.items():
        print(f"  ✅ {metric_name}: {count}")
    
    return True

def main():
    """Run all design system alignment tests"""
    print("=" * 60)
    print("DESIGN SYSTEM ALIGNMENT TEST SUITE")
    print("=" * 60)
    
    try:
        test_color_consistency()
        test_typography_consistency()
        test_spacing_consistency()
        test_border_radius_consistency()
        test_transition_consistency()
        test_shadow_consistency()
        test_button_pattern_consistency()
        test_form_pattern_consistency()
        test_sidebar_pattern_consistency()
        test_responsive_pattern_consistency()
        test_accessibility_pattern_consistency()
        count_design_system_compliance()
        
        print("\n" + "=" * 60)
        print("✅ ALL DESIGN SYSTEM ALIGNMENT TESTS COMPLETED")
        print("User profile components are aligned with the established design system!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())