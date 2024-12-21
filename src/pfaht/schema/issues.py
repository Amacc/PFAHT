"""
Issues Schema
=============
"""

from pydantic import BaseModel, computed_field
from enum import StrEnum
from . import api, index, services


class IssueTableCreatedResponse(api.ApiResponse[None]):
    message: str = "Issues table created"

    links: dict[str, index.Link] = {
        "Issues": index.Link(url="/issues", title="List Issues")
    }


class DeletedIssueResponse(api.ApiResponse[int]):
    message: str = "Issue Deleted"

    links: dict[str, index.Link] = {
        "Issues": index.Link(url="/issues", title="List Issues")
    }


class IssueStatus(StrEnum):
    """Enumeration of valid issue statuses"""

    OPEN = "open"
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"


class NewIssue(BaseModel):
    """
    New Issue Schema
    =================
    """

    issue_title: str
    issue_body: str
    issue_status: IssueStatus


class Issue(NewIssue):
    """
    Issue Schema
    ============
    """

    issue_id: int

    @property
    def _html_template(self):
        return "issue/item.html"

    def __str__(self):
        return self.issue_title

    def __repr__(self):
        return f"Issue({self.issue_title})"


class IssueListResponse(api.PagedApiResponse[Issue]):
    message: str = "List of Issues"

    links: dict[str, index.Link] = {
        "Issues": index.Link(url="/issues", title="Issues List")
    }

    @property
    def _title(self):
        return "Issue List"

    @property
    def _html_template(self):
        return "page/list.html"

    def model_post_init(self, __context):
        """Post-initialization hook

        After the model has been initialized, we will add the additional
        links for the issues list page.
        """
        if not self.page_options.page <= 1:
            prior_page_fragment = self.prior_page_fragment()
            self.links.update(
                Prior=index.Link(
                    url=f"/issues?{prior_page_fragment}",
                    title="Prior Page",
                )
            )
        next_page_fragment = self.next_page_fragment()
        self.links.update(
            Next=index.Link(
                url=f"/issues?{next_page_fragment}",
                title="Next Page",
            )
        )


class IssueResponse(api.ApiResponse[Issue]):
    """Issue Response Schema"""

    message: str = "Issue Details"

    links: dict[str, index.Link] = {
        "Issues": index.Link(url="/issues", title="Issues List")
    }

    @property
    def _html_template(self):
        return "page/detail.html"

    def model_post_init(self, __context):
        """Post-initialization hook

        After the model has been initialized, we will add the additional
        links for the issue page.
        """
        super().model_post_init(__context)
        self.links.update(
            Self=index.Link(url=f"/issues/{self.response.issue_id}", title="View Issue")
        )


class IssueServiceResponse(services.ServiceResponse[Issue]):
    """Issue Service Response Schema"""


class IssueListServiceResponse(services.ServiceResponseList[Issue]):
    """Issue List Service Response Schema"""
