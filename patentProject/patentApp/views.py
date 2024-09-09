from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from .models import Patent
from .serializers import PatentQuerySerializer, PatentSummarySerializer

# Function based view for query
@api_view(['GET'])
def query_patents(request):
    try:
        queryset = Patent.objects.all()

        # Extract query parameters
        assignee                = request.query_params.get('assignee', None)
        inventor                = request.query_params.get('inventor', None)
        filing_date_start       = request.query_params.get('filing_date_start', None)
        filing_date_end         = request.query_params.get('filing_date_end', None)
        publication_date_start  = request.query_params.get('publication_date_start', None)
        publication_date_end    = request.query_params.get('publication_date_end', None)

        # Validate and apply filters
        if assignee:
            queryset            = queryset.filter(assignee=assignee)

        if inventor:
            queryset            = queryset.filter(inventor=inventor)

        # Validate and apply date filters
        if filing_date_start and filing_date_end:
            start_date          = parse_date(filing_date_start)
            end_date            = parse_date(filing_date_end)
            if start_date and end_date:
                queryset        = queryset.filter(filing_date__range=(start_date, end_date))
            else:
                raise ValidationError("Invalid date format for filing date.")
        elif filing_date_start or filing_date_end:
            # Handle case where only one date is provided
            return Response({'error': 'Both filing_date_start and filing_date_end must be provided to filter by filing date.'}, status=status.HTTP_400_BAD_REQUEST)

        if publication_date_start and publication_date_end:
            start_date          = parse_date(publication_date_start)
            end_date            = parse_date(publication_date_end)
            if start_date and end_date:
                queryset        = queryset.filter(publication_date__range=(start_date, end_date))
            else:
                raise ValidationError("Invalid date format for publication date.")
        elif publication_date_start or publication_date_end:
            # Handle case where only one date is provided
            return Response({'error': 'Both publication_date_start and publication_date_end must be provided to filter by publication date.'}, status=status.HTTP_400_BAD_REQUEST)


        # Serialize and return the filtered queryset
        serializer = PatentQuerySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValidationError as ve:
        # Handle validation errors (e.g., invalid date format)
        return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Handle other unexpected errors
        return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Function based view for summary
@api_view(['GET'])
def patent_summary(request):
    try:
        # Aggregate counts by assignee
        count_by_assignee = (
            Patent.objects
            .values('assignee')
            .annotate(count=Count('id'))
            .order_by('-count')  # Order by count descending
        )
        
        # Get the assignee with the maximum count
        max_assignee = count_by_assignee[0] if count_by_assignee else {'assignee': None, 'count': 0}

        # Aggregate counts by inventor
        count_by_inventor = (
            Patent.objects
            .values('inventor')
            .annotate(count=Count('id'))
            .order_by('-count')  # Order by count descending
        )
        
        # Get the inventor with the maximum count
        max_inventor = count_by_inventor[0] if count_by_inventor else {'inventor': None, 'count': 0}

        # Aggregate dates with their associated assignee
        earliest_filing = (
            Patent.objects
            .order_by('filing_date')
            .values('patent_id', 'assignee', 'filing_date')
            .first()
        )
        latest_filing = (
            Patent.objects
            .order_by('-filing_date')
            .values('patent_id', 'assignee', 'filing_date')
            .first()
        )
        earliest_publication = (
            Patent.objects
            .order_by('publication_date')
            .values('patent_id', 'assignee', 'publication_date')
            .first()
        )
        latest_publication = (
            Patent.objects
            .order_by('-publication_date')
            .values('patent_id', 'assignee', 'publication_date')
            .first()
        )

        summary_data = {
            'total_patents'             : Patent.objects.count(),
            'max_assignee'              : max_assignee,
            'max_inventor'              : max_inventor,
            'earliest_filing_date'      : {
                'assignee_id'               : earliest_filing['patent_id'] if earliest_filing else None,
                'assignee_name'             : earliest_filing['assignee'] if earliest_filing else None,
                'date'                      : earliest_filing['filing_date'] if earliest_filing else None
            },
            'latest_filing_date'        : {
                'assignee_id'               : latest_filing['patent_id'] if latest_filing else None,
                'assignee_name'             : latest_filing['assignee'] if latest_filing else None,
                'date'                      : latest_filing['filing_date'] if latest_filing else None
            },
            'earliest_publication_date' : {
                'assignee_id'               : earliest_publication['patent_id'] if earliest_publication else None,
                'assignee_name'             : earliest_publication['assignee'] if earliest_publication else None,
                'date'                      : earliest_publication['publication_date'] if earliest_publication else None
            },
            'latest_publication_date'   : {
                'assignee_id'               : latest_publication['patent_id'] if latest_publication else None,
                'assignee_name'             : latest_publication['assignee'] if latest_publication else None,
                'date'                      : latest_publication['publication_date'] if latest_publication else None
            }
        }

        # Serialize the summary data
        serializer = PatentSummarySerializer(summary_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except ObjectDoesNotExist as e:
        return Response({'error': 'No data found: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)
    
    except ValueError as ve:
        return Response({'error': 'Value error: ' + str(ve)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)