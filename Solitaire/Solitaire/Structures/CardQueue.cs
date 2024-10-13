using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Solitaire
{
    public class CardQueueNode
    {
        public Card Data { get; set; }
        public CardQueueNode Next { get; set; }

        public CardQueueNode(Card data)
        {
            Data = data;
            Next = null;
        }
    }

    public class CardQueue
    {
        private CardQueueNode front;
        private CardQueueNode rear;

        public CardQueue()
        {
            front = rear = null;
        }

        public bool IsEmpty()
        {
            return front == null;
        }

        // Enqueue a card to the queue
        public void Enqueue(Card card)
        {
            CardQueueNode newNode = new CardQueueNode(card);

            // If the queue is empty, both front and rear will point to the new node
            if (rear != null)
            {
                rear.Next = newNode;
            }
            rear = newNode;
            if (front == null)
            {
                front = rear;
            }
        }

        // Dequeue a card from the queue
        public Card Dequeue()
        {
            if (IsEmpty())
                throw new InvalidOperationException("Queue is empty");

            Card dequeuedCard = front.Data;
            front = front.Next;

            // If the front becomes null, then the queue is empty
            if (front == null)
            {
                rear = null;
            }

            return dequeuedCard;
        }

        // Peek at the front card without removing it
        public Card Peek()
        {
            if (IsEmpty())
                throw new InvalidOperationException("Queue is empty");

            return front.Data;
        }
    }

}
