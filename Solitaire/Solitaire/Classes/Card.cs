using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Solitaire
{
    public class Card
    {
        public enum SuitType { Clubs, Diamonds, Hearts, Spades }
        public SuitType Suit { get; private set; }
        public int Rank { get; private set; }
        public bool IsFaceUp { get; private set; }

        public Card(SuitType suit, int rank)
        {
            Suit = suit;
            Rank = rank;
            IsFaceUp = false;
        }

        public void Flip()
        {
            IsFaceUp = !IsFaceUp;
        }
    }

}
