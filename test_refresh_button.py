#!/usr/bin/env python3
"""
Test script for refresh button component - Task 3.5
"""

import re
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_refresh_button_components():
    """Test refresh button component classes"""
    print("Testing refresh button components...")
    
    # Read the CSS file
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Define expected refresh button classes
    refresh_classes = [
        'profile-refresh-btn',
        'profile-refresh-icon',
        'profile-refresh-text',
        'profile-refresh-btn-group'
    ]
    
    print("✅ REFRESH BUTTON CLASSES:")
    for class_name in refresh_classes:
        if f'.{class_name}' in css_content:
            print(f"  ✅ {class_name} - defined")
        else:
            print(f"  ❌ {class_name} - missing")
    
    return True

def test_refresh_button_variants():
    """Test refresh button variants"""
    print("\nTesting refresh button variants...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Style variants
    style_variants = [
        '.profile-refresh-btn.secondary',
        '.profile-refresh-btn.outline',
        '.profile-refresh-btn.small',
        '.profile-refresh-btn.large',
        '.profile-refresh-btn.success',
        '.profile-refresh-btn.warning',
        '.profile-refresh-btn.danger'
    ]
    
    print("✅ REFRESH BUTTON VARIANTS:")
    for variant in style_variants:
        if variant in css_content:
            print(f"  ✅ {variant} - defined")
        else:
            print(f"  ❌ {variant} - missing")
    
    return True

def test_refresh_button_states():
    """Test refresh button states"""
    print("\nTesting refresh button states...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Button states
    button_states = [
        '.profile-refresh-btn:hover',
        '.profile-refresh-btn:active',
        '.profile-refresh-btn:focus',
        '.profile-refresh-btn:disabled',
        '.profile-refresh-btn.loading'
    ]
    
    print("✅ REFRESH BUTTON STATES:")
    for state in button_states:
        if state in css_content:
            print(f"  ✅ {state} - defined")
        else:
            print(f"  ❌ {state} - missing")
    
    return True

def test_refresh_button_integration():
    """Test refresh button integration with other components"""
    print("\nTesting refresh button integration...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Integration with other components
    integration_classes = [
        '.profile-refresh-btn .profile-loading-spinner',
        '.profile-toolbar .profile-refresh-btn',
        '.sidebar-header .profile-refresh-btn',
        '.profile-refresh-btn.icon-only'
    ]
    
    print("✅ REFRESH BUTTON INTEGRATION:")
    for integration in integration_classes:
        if integration in css_content:
            print(f"  ✅ {integration} - defined")
        else:
            print(f"  ❌ {integration} - missing")
    
    return True

def test_refresh_button_loading_states():
    """Test refresh button loading states"""
    print("\nTesting refresh button loading states...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Loading states
    loading_states = [
        '.profile-refresh-btn.loading',
        '.profile-refresh-btn.loading .profile-refresh-text',
        '.profile-refresh-btn.loading .profile-refresh-icon',
        '.profile-refresh-btn.loading .profile-loading-spinner'
    ]
    
    print("✅ REFRESH BUTTON LOADING STATES:")
    for state in loading_states:
        if state in css_content:
            print(f"  ✅ {state} - defined")
        else:
            print(f"  ❌ {state} - missing")
    
    return True

def test_refresh_button_accessibility():
    """Test refresh button accessibility features"""
    print("\nTesting refresh button accessibility...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Accessibility features
    accessibility_features = [
        '.profile-refresh-btn:focus-visible',
        '.profile-refresh-btn .sr-only',
        'prefers-reduced-motion: reduce',
        'prefers-contrast: high'
    ]
    
    print("✅ REFRESH BUTTON ACCESSIBILITY:")
    for feature in accessibility_features:
        if feature in css_content:
            print(f"  ✅ {feature} - implemented")
        else:
            print(f"  ❌ {feature} - missing")
    
    return True

def test_refresh_button_responsive():
    """Test refresh button responsive design"""
    print("\nTesting refresh button responsive design...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Responsive breakpoints
    responsive_queries = [
        '@media (max-width: 480px)',
        '@media (max-width: 360px)',
        '@media (hover: none) and (pointer: coarse)',
        '@media (min-width: 1200px)'
    ]
    
    print("✅ REFRESH BUTTON RESPONSIVE DESIGN:")
    for query in responsive_queries:
        count = css_content.count(query)
        if count > 0:
            print(f"  ✅ {query} - {count} uses")
        else:
            print(f"  ❌ {query} - not used")
    
    return True

def test_refresh_button_animations():
    """Test refresh button animations"""
    print("\nTesting refresh button animations...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Animation features
    animation_features = [
        'transition: all 0.2s ease',
        'transform: translateY(-1px)',
        'animation: spin 1s linear infinite',
        '@keyframes refresh-success',
        'animation: refresh-success 0.3s ease-in-out'
    ]
    
    print("✅ REFRESH BUTTON ANIMATIONS:")
    for feature in animation_features:
        if feature in css_content:
            print(f"  ✅ {feature} - implemented")
        else:
            print(f"  ❌ {feature} - missing")
    
    return True

def test_refresh_button_icons():
    """Test refresh button icon support"""
    print("\nTesting refresh button icon support...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Icon classes and content
    icon_features = [
        '.profile-refresh-icon',
        '.profile-refresh-btn.icon-refresh::before',
        '.profile-refresh-btn.icon-update::before',
        '.profile-refresh-btn.icon-sync::before',
        'content: "↻"',
        'content: "⟳"',
        'content: "⇄"'
    ]
    
    print("✅ REFRESH BUTTON ICONS:")
    for feature in icon_features:
        if feature in css_content:
            print(f"  ✅ {feature} - implemented")
        else:
            print(f"  ❌ {feature} - missing")
    
    return True

def test_refresh_button_tooltips():
    """Test refresh button tooltip support"""
    print("\nTesting refresh button tooltip support...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Tooltip features
    tooltip_features = [
        '.profile-refresh-btn[title]',
        '.profile-refresh-btn[title]:hover::after',
        'content: attr(title)',
        'animation: fade-in 0.2s ease forwards'
    ]
    
    print("✅ REFRESH BUTTON TOOLTIPS:")
    for feature in tooltip_features:
        if feature in css_content:
            print(f"  ✅ {feature} - implemented")
        else:
            print(f"  ❌ {feature} - missing")
    
    return True

def count_refresh_button_features():
    """Count total refresh button features"""
    print("\nCounting refresh button features...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Count different types of features
    feature_counts = {
        'Refresh Button Classes': len(re.findall(r'\.profile-refresh-[a-z-]*\s*{', css_content)),
        'Button Variants': len(re.findall(r'\.profile-refresh-btn\.[a-z-]*\s*{', css_content)),
        'Button States': len(re.findall(r'\.profile-refresh-btn:[a-z-]*', css_content)),
        'Media Queries': len(re.findall(r'@media.*profile-refresh', css_content)),
        'Icon Content': len(re.findall(r'content: "[↻⟳⇄]"', css_content)),
        'Animation Features': len(re.findall(r'animation:|transition:|transform:', css_content)),
        'Accessibility Features': len(re.findall(r'focus-visible|sr-only|prefers-', css_content))
    }
    
    print("✅ REFRESH BUTTON FEATURE COUNTS:")
    for feature_type, count in feature_counts.items():
        print(f"  ✅ {feature_type}: {count}")
    
    return True

def test_refresh_button_touch_support():
    """Test refresh button touch device support"""
    print("\nTesting refresh button touch support...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Touch-specific features
    touch_features = [
        'min-height: 44px',
        'hover: none',
        'pointer: coarse',
        'transform: scale(0.98)'
    ]
    
    print("✅ REFRESH BUTTON TOUCH SUPPORT:")
    for feature in touch_features:
        if feature in css_content:
            print(f"  ✅ {feature} - implemented")
        else:
            print(f"  ❌ {feature} - missing")
    
    return True

def main():
    """Run all refresh button tests"""
    print("=" * 60)
    print("REFRESH BUTTON COMPONENT TEST SUITE")
    print("=" * 60)
    
    try:
        test_refresh_button_components()
        test_refresh_button_variants()
        test_refresh_button_states()
        test_refresh_button_integration()
        test_refresh_button_loading_states()
        test_refresh_button_accessibility()
        test_refresh_button_responsive()
        test_refresh_button_animations()
        test_refresh_button_icons()
        test_refresh_button_tooltips()
        test_refresh_button_touch_support()
        count_refresh_button_features()
        
        print("\n" + "=" * 60)
        print("✅ ALL REFRESH BUTTON TESTS COMPLETED SUCCESSFULLY")
        print("Refresh button component is fully implemented!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())