using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Solitaire
{
    public class Deck
    {
        private List<Card> cards;

        public Deck()
        {
            cards = new List<Card>();
            foreach (Card.SuitType suit in Enum.GetValues(typeof(Card.SuitType)))
            {
                for (int rank = 1; rank <= 13; rank++)
                {
                    cards.Add(new Card(suit, rank));
                }
            }
        }

        public void Shuffle()
        {
            Random rng = new Random();
            cards = cards.OrderBy(x => rng.Next()).ToList();
        }

        public Card DrawCard()
        {
            if (cards.Count > 0)
            {
                var card = cards[0];
                cards.RemoveAt(0);
                return card;
            }
            return null;
        }
    }

}
