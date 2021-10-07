from __future__ import annotations

from typing import List

from django.db import models
from django.db.models import Model


class PageableQuerySet(models.query.QuerySet):
    """
       활용 예제

       ```
           o_queryset = Order.objects.paging(strategy=Paging.CursorBased /* <-Enum임 */)
           o_list1 = o_queryset.next()
           o_list2 = o_queryset.next()
           o_list3 = o_queryset.next()
       ```

       이 페이징 QuerySet 메서드는 이렇게 만든 현재 코드도 꽤 쓸만한 방식이지만 제가 임시로 만든거라 아직 아쉽습니다.

       * Pagination 전략을 선택할수 있도록 QuerySet자체를 PaginationQuerySet을 만들어서
         상속 관계를 가지게하거나 args로 옵션을 받아서 아래와 같이 작성가능하도록 구현해도 좋습니다.

       나는 이를 경이로운 방법으로 구현했으나 코드에 여백이 부족해 적지 않는다.
    """

    _default_start_pk = -1
    _default_page_size = 10

    def pageable(self, start_pk=None) -> PageableQuerySet:
        """
            Cursor Based Pagination
        """
        s_pk = start_pk or self._default_start_pk
        return self.filter(id__gt=s_pk)

    def next(self, page_size=None) -> List[Model]:

        p_size = page_size or self._default_page_size
        paged_list = list(self.filter(id__gt=self._default_start_pk)[:p_size])
        if paged_list:
            self._default_start_pk = paged_list[-1].pk
        return paged_list