using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Solitaire
{
    public class CardStackNode
    {
        public Card Data { get; set; }
        public CardStackNode Next { get; set; }

        public CardStackNode(Card data)
        {
            Data = data;
            Next = null;
        }
    }

    public class CardStack
    {
        private CardStackNode top;

        public CardStack()
        {
            top = null;
        }

        public bool IsEmpty()
        {
            return top == null;
        }

        
        public void Push(Card card)
        {
            CardStackNode newNode = new CardStackNode(card);
            newNode.Next = top;
            top = newNode;
        }

        
        public Card Pop()
        {
            if (IsEmpty())
                throw new InvalidOperationException("Stack is empty");

            Card poppedCard = top.Data;
            top = top.Next;
            return poppedCard;
        }

        
        public Card Peek()
        {
            if (IsEmpty())
                throw new InvalidOperationException("Stack is empty");

            return top.Data;
        }
    }

}
