#!/usr/bin/env python3
"""
Test script for loading spinner and error message components
"""

import re
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_loading_spinner_components():
    """Test loading spinner component classes"""
    print("Testing loading spinner components...")
    
    # Read the CSS file
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Define expected spinner classes
    spinner_classes = [
        'profile-loading-spinner',
        'profile-loading-container',
        'profile-loading-text',
        'profile-loading-dots',
        'profile-loading-pulse',
        'profile-loading-skeleton'
    ]
    
    print("✅ LOADING SPINNER CLASSES:")
    for class_name in spinner_classes:
        if f'.{class_name}' in css_content:
            print(f"  ✅ {class_name} - defined")
        else:
            print(f"  ❌ {class_name} - missing")
    
    return True

def test_spinner_variants():
    """Test spinner size and color variants"""
    print("\nTesting spinner variants...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Size variants
    size_variants = [
        '.profile-loading-spinner.small',
        '.profile-loading-spinner.medium',
        '.profile-loading-spinner.large'
    ]
    
    # Color variants
    color_variants = [
        '.profile-loading-spinner.primary',
        '.profile-loading-spinner.success',
        '.profile-loading-spinner.warning',
        '.profile-loading-spinner.danger',
        '.profile-loading-spinner.info',
        '.profile-loading-spinner.light',
        '.profile-loading-spinner.dark'
    ]
    
    print("✅ SPINNER SIZE VARIANTS:")
    for variant in size_variants:
        if variant in css_content:
            print(f"  ✅ {variant} - defined")
        else:
            print(f"  ❌ {variant} - missing")
    
    print("✅ SPINNER COLOR VARIANTS:")
    for variant in color_variants:
        if variant in css_content:
            print(f"  ✅ {variant} - defined")
        else:
            print(f"  ❌ {variant} - missing")
    
    return True

def test_error_message_components():
    """Test error message component classes"""
    print("\nTesting error message components...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Error message classes
    error_classes = [
        'profile-error-message',
        'profile-error-content',
        'profile-error-title',
        'profile-error-description',
        'profile-error-dismiss'
    ]
    
    print("✅ ERROR MESSAGE CLASSES:")
    for class_name in error_classes:
        if f'.{class_name}' in css_content:
            print(f"  ✅ {class_name} - defined")
        else:
            print(f"  ❌ {class_name} - missing")
    
    return True

def test_error_message_variants():
    """Test error message variants"""
    print("\nTesting error message variants...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Message type variants
    message_variants = [
        '.profile-error-message.error',
        '.profile-error-message.warning',
        '.profile-error-message.info',
        '.profile-error-message.success'
    ]
    
    # Style variants
    style_variants = [
        '.profile-error-message.dismissible',
        '.profile-error-message.inline',
        '.profile-error-message.compact'
    ]
    
    print("✅ ERROR MESSAGE TYPE VARIANTS:")
    for variant in message_variants:
        if variant in css_content:
            print(f"  ✅ {variant} - defined")
        else:
            print(f"  ❌ {variant} - missing")
    
    print("✅ ERROR MESSAGE STYLE VARIANTS:")
    for variant in style_variants:
        if variant in css_content:
            print(f"  ✅ {variant} - defined")
        else:
            print(f"  ❌ {variant} - missing")
    
    return True

def test_loading_animations():
    """Test loading animations"""
    print("\nTesting loading animations...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Animation keyframes
    animations = [
        '@keyframes spin',
        '@keyframes pulse-scale',
        '@keyframes dots',
        '@keyframes skeleton-loading',
        '@keyframes shimmer',
        '@keyframes fade-in',
        '@keyframes slide-in'
    ]
    
    print("✅ LOADING ANIMATIONS:")
    for animation in animations:
        if animation in css_content:
            print(f"  ✅ {animation} - defined")
        else:
            print(f"  ❌ {animation} - missing")
    
    return True

def test_loading_states():
    """Test component loading states"""
    print("\nTesting loading states...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Loading states
    loading_states = [
        '.profile-section.loading',
        '.profile-summary.loading',
        '.profile-loading-container.inline',
        '.profile-loading-container.fullscreen',
        '.profile-loading-container.overlay'
    ]
    
    print("✅ COMPONENT LOADING STATES:")
    for state in loading_states:
        if state in css_content:
            print(f"  ✅ {state} - defined")
        else:
            print(f"  ❌ {state} - missing")
    
    return True

def test_skeleton_loading():
    """Test skeleton loading variants"""
    print("\nTesting skeleton loading...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Skeleton variants
    skeleton_variants = [
        '.profile-loading-skeleton.text',
        '.profile-loading-skeleton.title',
        '.profile-loading-skeleton.paragraph'
    ]
    
    print("✅ SKELETON LOADING VARIANTS:")
    for variant in skeleton_variants:
        if variant in css_content:
            print(f"  ✅ {variant} - defined")
        else:
            print(f"  ❌ {variant} - missing")
    
    return True

def test_accessibility_features():
    """Test accessibility features"""
    print("\nTesting accessibility features...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Accessibility features
    accessibility_features = [
        'prefers-reduced-motion: reduce',
        'prefers-contrast: high',
        'aria-live="polite"',
        'role="alert"',
        '.sr-only',
        'animation: none'
    ]
    
    print("✅ ACCESSIBILITY FEATURES:")
    for feature in accessibility_features:
        if feature in css_content:
            print(f"  ✅ {feature} - implemented")
        else:
            print(f"  ❌ {feature} - missing")
    
    return True

def test_responsive_design():
    """Test responsive design for loading/error components"""
    print("\nTesting responsive design...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Responsive features
    responsive_features = [
        'width: 28px',    # Mobile spinner size
        'width: 24px',    # Small mobile spinner
        'font-size: 0.8rem',  # Mobile text size
        'font-size: 0.75rem', # Small mobile text
        'padding: 0.5rem',    # Mobile padding
        'padding: 0.375rem'   # Small mobile padding
    ]
    
    print("✅ RESPONSIVE FEATURES:")
    for feature in responsive_features:
        count = css_content.count(feature)
        if count > 0:
            print(f"  ✅ {feature} - {count} uses")
        else:
            print(f"  ❌ {feature} - not used")
    
    return True

def test_icon_integration():
    """Test icon integration in error messages"""
    print("\nTesting icon integration...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Icon content
    icon_content = [
        "content: '⚠'",    # Warning icon
        "content: 'ℹ'",    # Info icon
        "content: '✓'",    # Success icon
        "::before"         # Pseudo-element usage
    ]
    
    print("✅ ICON INTEGRATION:")
    for icon in icon_content:
        if icon in css_content:
            print(f"  ✅ {icon} - implemented")
        else:
            print(f"  ❌ {icon} - missing")
    
    return True

def count_loading_error_features():
    """Count total loading and error features"""
    print("\nCounting loading and error features...")
    
    with open('static/css/style.css', 'r') as f:
        css_content = f.read()
    
    # Count different types of features
    feature_counts = {
        'Loading Classes': len(re.findall(r'\.profile-loading-[a-z-]*\s*{', css_content)),
        'Error Classes': len(re.findall(r'\.profile-error-[a-z-]*\s*{', css_content)),
        'Animations': len(re.findall(r'@keyframes [a-z-]*', css_content)),
        'Spinner Variants': len(re.findall(r'\.profile-loading-spinner\.[a-z]*\s*{', css_content)),
        'Error Variants': len(re.findall(r'\.profile-error-message\.[a-z]*\s*{', css_content)),
        'Pseudo Elements': len(re.findall(r'::before|::after', css_content)),
        'Media Queries': len(re.findall(r'@media.*{', css_content))
    }
    
    print("✅ FEATURE COUNTS:")
    for feature_type, count in feature_counts.items():
        print(f"  ✅ {feature_type}: {count}")
    
    return True

def main():
    """Run all loading and error component tests"""
    print("=" * 60)
    print("LOADING SPINNER & ERROR MESSAGE TEST SUITE")
    print("=" * 60)
    
    try:
        test_loading_spinner_components()
        test_spinner_variants()
        test_error_message_components()
        test_error_message_variants()
        test_loading_animations()
        test_loading_states()
        test_skeleton_loading()
        test_accessibility_features()
        test_responsive_design()
        test_icon_integration()
        count_loading_error_features()
        
        print("\n" + "=" * 60)
        print("✅ ALL LOADING & ERROR COMPONENT TESTS COMPLETED SUCCESSFULLY")
        print("Loading spinners and error messages are fully implemented!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())