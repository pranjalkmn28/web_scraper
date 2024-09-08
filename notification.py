class Communication:
    @staticmethod
    def notify(scraped_count, updated_count):
        """Notify the number of products scraped and saved."""
        print(f"{scraped_count} products scraped and {updated_count} products updated in the database.")
