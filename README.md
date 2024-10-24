# Code_Quest
    Replace `app.py` with the name of your main application file.
6.  **Access the Application**
    Open your web browser and go to `http://127.0.0.1:5000` to access the Flipkart Product Price Tracker.

## Usage

*   **Fetch Product Details**: Enter the product URL in the input field and click on "Fetch Details" to retrieve product information.
*   **Track Products**: The tracked products will be displayed below, showing their titles, prices, descriptions, reviews, and links to view them on Flipkart.
*   **Recheck Price**: Click the "Recheck Price" button for any product to update its price.
*   **View Price History**: Click on a product to view its price history.
*   **Search and Filter**: Use the search bar to find products by title and the filter option to narrow down products by price range.

## Database Schema

The application uses a SQLite database to store product data. The database schema consists of two tables:

*   **products**: Stores product information, including product ID, title, description, price, reviews, and link to view on Flipkart.
*   **price_history**: Stores the price history of tracked products, including product ID, price, and date.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

*   Flipkart Affiliate Program for providing the API to fetch product details.
*   Flask for the web framework.
*   SQLite for the database management system.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or suggestions.