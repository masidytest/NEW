# plugins/weather.py
# Weather plugin (stub - can be connected to real API)

def register(cap_registry):
    """Register weather plugin capabilities"""
    
    def tool_get_weather(location: str = "New York") -> str:
        """
        Get weather for a location (stub implementation)
        In production, connect to OpenWeatherMap, WeatherAPI, etc.
        """
        # Stub data
        weather_data = {
            "new york": "Sunny, 72°F",
            "london": "Cloudy, 15°C",
            "tokyo": "Rainy, 18°C",
            "paris": "Partly cloudy, 20°C",
        }
        
        location_lower = location.lower()
        return weather_data.get(location_lower, f"Weather data not available for {location}")
    
    def tool_get_forecast(location: str = "New York", days: int = 3) -> str:
        """
        Get weather forecast (stub implementation)
        """
        return f"3-day forecast for {location}: Day 1: Sunny, Day 2: Cloudy, Day 3: Rainy"
    
    # Register capabilities
    cap_registry.register(
        name="get_weather",
        func=tool_get_weather,
        tags=["weather", "api", "plugin"],
        input_schema={"location": "str"},
        output_schema={"weather": "str"},
        description="Get current weather for a location (plugin)"
    )
    
    cap_registry.register(
        name="get_forecast",
        func=tool_get_forecast,
        tags=["weather", "api", "plugin"],
        input_schema={"location": "str", "days": "int"},
        output_schema={"forecast": "str"},
        description="Get weather forecast for a location (plugin)"
    )
