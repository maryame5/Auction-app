Auction Site

An auction platform built using Django that allows users to create, view, bid on, and comment on auction listings. Users can also maintain a personalized watchlist and explore listings by category.

Features

1. Models

The application includes the following models:

Auction Listings: Contains fields such as title, description, starting bid, current price, image URL, category, and status (active/closed).

Bids: Tracks bids placed on listings, including the bidder and the bid amount.

Comments: Stores user comments associated with specific listings.

Additional models may be included as needed.

2. Create Listing

Users can create a new auction listing by specifying:

Title and description of the listing.

Starting bid amount.

Optionally, an image URL and a category (e.g., Fashion, Electronics, etc.).

3. Active Listings Page

The homepage displays all currently active auction listings, showing:

Title and description.

Current price.

Photo (if provided).

4. Listing Page

Clicking on a listing directs users to a detailed page for that specific listing, which displays:

All details about the listing.

Current price.

Comments.

Signed-in users can:

Add or remove the listing from their watchlist.

Place bids (must meet minimum bid criteria).

Add comments.

The creator of the listing can:

Close the auction, marking the highest bidder as the winner and deactivating the listing.

For closed listings, winning users are notified if they have won the auction.

5. Watchlist

Users can view their watchlist, which displays all listings they have added.

Clicking a listing from the watchlist redirects to the listing page.

6. Categories

A dedicated page displays all available listing categories.

Clicking on a category name shows all active listings within that category.

7. Django Admin Interface

The admin interface allows site administrators to:

View, add, edit, and delete any listings.

Manage comments and bids made on the site.
