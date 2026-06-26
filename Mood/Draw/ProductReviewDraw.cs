using Mood.EF2;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Mood.Draw
{
    public class ProductReviewDraw
    {
        private readonly QuanLySachDBContext db;

        public ProductReviewDraw()
        {
            db = new QuanLySachDBContext();
        }

        public List<ProductReview> ListByProduct(long productId)
        {
            return db.ProductReviews
                .Where(x => x.ProductID == productId && x.Status)
                .OrderByDescending(x => x.CreatedAt)
                .ToList();
        }

        public double AverageRating(long productId)
        {
            var query = db.ProductReviews.Where(x => x.ProductID == productId && x.Status);
            return query.Any() ? query.Average(x => x.Rating) : 0;
        }

        public int CountByProduct(long productId)
        {
            return db.ProductReviews.Count(x => x.ProductID == productId && x.Status);
        }

        public bool Upsert(ProductReview review)
        {
            var productExists = db.Sanphams.Any(x => x.IDContent == review.ProductID && x.Status);
            var userExists = db.Users.Any(x => x.IDUser == review.UserID && x.Status);
            if (!productExists || !userExists || review.Rating < 1 || review.Rating > 5 || string.IsNullOrWhiteSpace(review.Comment))
            {
                return false;
            }

            var current = db.ProductReviews.FirstOrDefault(x => x.ProductID == review.ProductID && x.UserID == review.UserID);
            if (current == null)
            {
                review.CreatedAt = DateTime.Now;
                review.Comment = review.Comment.Trim();
                review.Status = true;
                db.ProductReviews.Add(review);
            }
            else
            {
                current.Rating = review.Rating;
                current.Comment = review.Comment.Trim();
                current.UserName = review.UserName;
                current.CreatedAt = DateTime.Now;
                current.Status = true;
            }

            db.SaveChanges();
            return true;
        }
    }
}
