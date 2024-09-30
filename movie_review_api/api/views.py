from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.shortcuts import get_object_or_404
from movies.models import Review
from .serializer import ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])  # Make sure only authenticated users can modify or delete reviews
def paginated_reviews_list(request, movie_title, review_id=None):
    # GET: Retrieve all reviews for a specific movie with pagination
    if request.method == 'GET':
        reviews = Review.objects.filter(movie_title=movie_title)
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Number of reviews per page
        result_page = paginator.paginate_queryset(reviews, request)
    
        # Serialize the paginated data
        serializer = ReviewSerializer(result_page, many=True)
    
        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
    
    # POST: Add a new review for a specific movie
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Update an existing review (requires review_id)
    elif request.method == 'PUT':
        if review_id is None:
            return Response({'error': 'Review ID required for update'}, status=status.HTTP_400_BAD_REQUEST)
        
        review = get_object_or_404(Review, id=review_id, user_id=request.user.id)
        serializer = ReviewSerializer(review, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE: Remove an existing review (requires review_id)
    elif request.method == 'DELETE':
        if review_id is None:
            return Response({'error': 'Review ID required for deletion'}, status=status.HTTP_400_BAD_REQUEST)

        review = get_object_or_404(Review, id=review_id, user_id=request.user.id)
        review.delete()
        return Response({'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
