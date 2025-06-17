#!/usr/bin/env python3
"""
Standalone test for the persona system functionality
"""

import sys
import os
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.persona_system import get_all_personas, get_persona_by_id, get_persona_system_prompt
    print("✅ Successfully imported persona system modules")
except ImportError as e:
    print(f"❌ Failed to import persona system modules: {e}")
    sys.exit(1)

def test_get_all_personas():
    """Test that we can load all personas"""
    print("\n🔍 Testing get_all_personas()...")
    
    try:
        personas = get_all_personas()
        assert isinstance(personas, dict), f"Expected dict, got {type(personas)}"
        assert len(personas) > 0, "No personas found"
        
        print(f"✅ Found {len(personas)} personas:")
        for persona_id, persona_data in personas.items():
            print(f"   - {persona_id}: {persona_data.get('name', 'Unknown')}")
            
        return True, personas
    except Exception as e:
        print(f"❌ get_all_personas() failed: {e}")
        return False, {}

def test_get_persona_by_id(personas):
    """Test getting individual personas by ID"""
    print("\n🔍 Testing get_persona_by_id()...")
    
    success_count = 0
    total_count = len(personas)
    
    for persona_id in personas.keys():
        try:
            persona_data = get_persona_by_id(persona_id)
            
            # Validate persona structure
            required_fields = ['name', 'description', 'voice_id']
            for field in required_fields:
                assert field in persona_data, f"Missing field '{field}' in persona {persona_id}"
            
            print(f"✅ {persona_id}: {persona_data['name']} - {persona_data['voice_id']}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Failed to get persona {persona_id}: {e}")
    
    print(f"📊 Persona retrieval: {success_count}/{total_count} successful")
    return success_count == total_count

def test_persona_system_prompt(personas):
    """Test generating system prompts for personas"""
    print("\n🔍 Testing get_persona_system_prompt()...")
    
    success_count = 0
    
    # Test with a sample persona
    sample_persona_id = next(iter(personas.keys()))
    sample_persona = get_persona_by_id(sample_persona_id)
    
    try:
        system_prompt = get_persona_system_prompt(sample_persona)
        assert isinstance(system_prompt, str), f"Expected string, got {type(system_prompt)}"
        assert len(system_prompt) > 100, "System prompt seems too short"
        
        print(f"✅ Generated system prompt for {sample_persona['name']}")
        print(f"   Prompt length: {len(system_prompt)} characters")
        print(f"   Preview: {system_prompt[:150]}...")
        
        success_count += 1
    except Exception as e:
        print(f"❌ Failed to generate system prompt for {sample_persona_id}: {e}")
    
    # Test with None input
    try:
        default_prompt = get_persona_system_prompt(None)
        if default_prompt is not None:
            print(f"✅ Default system prompt: {len(default_prompt)} characters")
        else:
            print("✅ None input correctly returns None")
        success_count += 1
    except Exception as e:
        print(f"❌ Failed to handle None input: {e}")
    
    return success_count == 2

def test_persona_data_structure(personas):
    """Test the structure and validity of persona data"""
    print("\n🔍 Testing persona data structure...")
    
    valid_personas = 0
    issues = []
    
    for persona_id, persona_data in personas.items():
        try:
            # Check required fields
            required_fields = ['name', 'description', 'voice_id']
            for field in required_fields:
                if field not in persona_data:
                    issues.append(f"{persona_id} missing '{field}'")
                    continue
            
            # Check field types
            if not isinstance(persona_data['name'], str):
                issues.append(f"{persona_id} 'name' is not a string")
            
            if not isinstance(persona_data['description'], str):
                issues.append(f"{persona_id} 'description' is not a string")
            
            if not isinstance(persona_data['voice_id'], str):
                issues.append(f"{persona_id} 'voice_id' is not a string")
            
            # Check optional characteristics
            if 'characteristics' in persona_data:
                characteristics = persona_data['characteristics']
                if not isinstance(characteristics, dict):
                    issues.append(f"{persona_id} 'characteristics' is not a dict")
                else:
                    # Check common characteristic fields
                    expected_chars = ['personality_traits', 'speaking_style', 'background', 'worldview']
                    char_count = sum(1 for char in expected_chars if char in characteristics)
                    if char_count > 0:
                        print(f"   {persona_id}: {char_count}/{len(expected_chars)} characteristic fields")
            
            valid_personas += 1
            
        except Exception as e:
            issues.append(f"{persona_id}: {str(e)}")
    
    if issues:
        print("⚠️  Data structure issues found:")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more issues")
    
    print(f"📊 Valid personas: {valid_personas}/{len(personas)}")
    return len(issues) == 0

def main():
    """Run all persona system tests"""
    print("🧪 Starting Standalone Persona System Tests")
    print("=" * 50)
    
    # Test 1: Load all personas
    success, personas = test_get_all_personas()
    if not success:
        print("❌ Basic persona loading failed, aborting further tests")
        return False
    
    # Test 2: Get individual personas
    success = test_get_persona_by_id(personas)
    if not success:
        print("⚠️  Some personas failed individual retrieval")
    
    # Test 3: Test system prompt generation
    success = test_persona_system_prompt(personas)
    if not success:
        print("⚠️  System prompt generation has issues")
    
    # Test 4: Validate data structure
    success = test_persona_data_structure(personas)
    if not success:
        print("⚠️  Some persona data structure issues found")
    
    print("\n" + "=" * 50)
    print("🎉 Persona system tests completed!")
    print(f"📁 Found {len(personas)} personas in the system")
    
    # Summary of available personas
    print("\n📋 Available Personas Summary:")
    for persona_id, persona_data in personas.items():
        name = persona_data.get('name', 'Unknown')
        voice = persona_data.get('voice_id', 'Unknown')
        desc_preview = persona_data.get('description', '')[:60] + "..." if len(persona_data.get('description', '')) > 60 else persona_data.get('description', '')
        print(f"   🎭 {name} ({persona_id}) - Voice: {voice}")
        print(f"      {desc_preview}")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 