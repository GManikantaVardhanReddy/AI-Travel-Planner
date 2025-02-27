# AI-Travel-Planner

Hey there! Welcome to **Travel Planner Pro**—a little app I built to make trip planning a breeze. Whether you’re dreaming of a quick weekend getaway or a big international adventure, this tool’s got your back. It uses AI to whip up detailed itineraries, checks the weather, and even lets you set your budget in whatever currency you’re rolling with. Cool, right?

## What’s This All About?

This is a web app I made with Streamlit (super easy to use!) that helps you plan trips. You tell it where you’re starting, where you’re going, how long you’re staying, and how much cash you’ve got, and it does the heavy lifting. It’ll suggest travel options, places to crash, and cool stuff to see—all while keeping your budget in check. Oh, and it throws in a map and weather forecast too, so you’re not caught off guard by a surprise rainstorm.

## How to Get It Running

Wanna give it a spin? Here’s how to set it up on your own machine:

1. **Grab the Code**: Clone this repo to your computer. Open your terminal and type:https://github.com/GManikantaVardhanReddy/AI-travel-planner.git
2. **Install the Stuff It Needs**: You’ll need a few Python libraries. Pop this into your terminal:
 That’ll grab everything listed in `requirements.txt`—think Streamlit, some AI bits, and map tools.

3. **Add Your API Key**: The AI magic comes from Google’s Gemini model, so you’ll need a Google API key. Get one from [Google Cloud](https://console.cloud.google.com/), then open `app.py` and replace `YOUR_GOOGLE_API_KEY_HERE` with your key. Save it!

4. **Fire It Up**: Run this in your terminal from the project folder:

   Your browser should pop open with the app. If not, just go to `http://localhost:8501`.

## What It Can Do

Here’s the fun stuff this app brings to the table:
- **AI-Powered Plans**: Tell it your trip details, and it spits out a full itinerary—travel options, places to stay, and must-see spots with costs.
- **Pick Your Currency**: Budget in INR, EUR, GBP, JPY, whatever! It converts everything to USD behind the scenes to keep things smooth.
- **Weather Check**: See what the weather’s like at your destination on travel day.
- **Fancy Map**: A little interactive map shows your start and end points with a line connecting them. Zoom around and feel like a pro explorer.
- **Download Your Plan**: Save your itinerary as a JSON file to keep or share.

## What You’ll Need
- Python (3.7 or higher works great)
- A Google API key (for the AI part)
- The libraries in `requirements.txt`:
- `streamlit`
- `langchain-google-genai`
- `streamlit-lottie`
- `requests`
- `pydeck`
- `geopy`
- `openmeteo-requests`

## Heads Up
- The currency rates in the app are static (as of Feb 2025). They’re close enough for fun, but if you want spot-on numbers, you’d need to hook up a real-time exchange rate API like [exchangerate-api.com](https://www.exchangerate-api.com/). I can help with that if you’re interested!
- If something breaks (like the weather API or geocoding), it’ll let you know with a warning but keep chugging along.

## How to Use It
1. Pick your starting point and destination.
2. Set your travel date and how many days you’re staying.
3. Enter your budget and choose your currency (INR, USD, etc.).
4. Pick your fave way to travel (flight, train, whatever).
5. Hit “Plan My Trip” and watch it go!

You’ll get a detailed plan, a weather peek, a map, and a download button for your itinerary. Easy peasy.

## Why I Made This
I love traveling but hate the planning grind—searching for flights, figuring out costs, all that jazz. So I thought, why not let AI handle it? Plus, I wanted something that works with any currency since I’ve got friends all over the place. This is the result—hope you like it!

## Wanna Help Out?
If you’ve got ideas to make this better—like adding more currencies, tweaking the design, or plugging in live exchange rates—feel free to fork this repo and send a pull request. I’d love to see what you come up with!

## Say Hi
Got questions or just wanna chat about travel? Hit me up on GitHub or wherever you find me. Happy adventuring!

---

© 2025 AI Travel Planner 
