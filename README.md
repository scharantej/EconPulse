## Flask Application Design for Economic Event Monitoring

### HTML Files

- **index.html:** This is the homepage of the application. It displays a newsfeed of upcoming economic events, their projected impact on the market, and a subscription form for real-time updates.
- **subscribe.html:** This page allows users to subscribe to specific economic indicators for real-time updates. It includes a form for entering an email address and selecting the indicators to subscribe to.
- **profile.html:** This page displays the list of indicators that a user has subscribed to, and allows them to manage their subscriptions.

### Routes

- **@app.route('/')** : This route renders the index.html page.
- **@app.route('/subscribe')** : This route renders the subscribe.html page.
- **@app.route('/profile')** : This route renders the profile.html page.
- **@app.route('/subscribe/submit', methods=['POST'])** : This route processes the submission from the subscribe.html page and adds the user's email address and selected indicators to a database.
- **@app.route('/profile/update', methods=['POST'])** : This route processes the submission from the profile.html page and updates the user's subscriptions.
- **@app.route('/events/upcoming')** : This route fetches upcoming economic events from an API or database and returns them in a JSON format.
- **@app.route('/events/subscribe')** : This route subscribes a user to real-time updates for a specific economic indicator.
- **@app.route('/events/unsubscribe')** : This route unsubscribes a user from real-time updates for a specific economic indicator.