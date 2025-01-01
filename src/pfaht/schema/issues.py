"""
Issues Schema
=============
"""

from pydantic import BaseModel, computed_field
from enum import StrEnum
from . import api, index, services, devices

IssueId = int


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
    IN_PROGRESS = "in-progress"
    PENDING = "pending"


class NewIssue(BaseModel):
    """
    New Issue Schema
    =================
    """

    issue_title: str
    issue_body: str
    issue_status: IssueStatus


class DefaultIssue(NewIssue):
    """A default issue for the form."""

    issue_title: str = "New Issue"
    issue_body: str = "Please enter a description of the issue."
    issue_status: IssueStatus = IssueStatus.OPEN

    @property
    def _is_editing(self):
        """When returned as html this will set the alpine data context."""
        return True


class Issue(NewIssue):
    """
    Issue Schema
    ============
    """

    issue_id: int

    @property
    def _is_editing(self):
        """When returned as html this will set the alpine data context."""
        return False

    def __str__(self):
        return self.issue_title

    def __repr__(self):
        return f"Issue({self.issue_title})"


class IssueListResponse(api.PagedApiResponse[Issue]):
    message: str = "List of Issues"
    _header_links: list[str] = {
        "NewForm": index.Link(url="/issues/new", title="New Issue"),
    }

    links: dict[str, index.Link] = {
        "Issues": index.Link(url="/issues", title="Issues List"),
        "New": index.Link(url="/issues", title="New Issue", method="POST"),
    }

    @property
    def title(self):
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
        if len(self.response) == self.page_options.per_page:
            next_page_fragment = self.next_page_fragment()
            self.links.update(
                Next=index.Link(
                    url=f"/issues?{next_page_fragment}",
                    title="Next Page",
                )
            )
        self.links.update(
            Add=index.Link(url="/issues/", title="New Issue", method="POST")
        )


class DefaultIssueResponse(api.ApiResponse[DefaultIssue]):
    """Issue Response Schema"""

    message: str = "Issue Details"

    links: dict[str, index.Link] = {
        "Issues": index.Link(url="/issues", title="Issues List")
    }

    @property
    def _html_template(self):
        return "page/detail.html"


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


class MissingIssuesResponse(api.ApiResponse[None]):
    """Returned when a requested issue is not found."""

    message: str = "Issue not found"


class RelatedDevicesResponse(api.PagedApiResponse[devices.Device]):
    """Related Devices Response Schema"""

    issue_id: int
    """The ID of the issue the devices are related to."""

    def model_post_init(self, __context):
        self.links.update(
            Issue=index.Link(url=f"/issues/{self.issue_id}", title="View Issue")
        )

    @property
    def title(self):
        return "Related Devices"

    @property
    def _html_template(self):
        return "page/list.html"


class IssueServiceResponse(services.ServiceResponse[Issue]):
    """Issue Service Response Schema"""


class RelateIssueServiceResponse(
    services.ServiceResponse[tuple[IssueId, devices.DeviceId]]
):
    """"""


class RelatedDevice(BaseModel):
    """Related Device Schema"""

    device_id: int


class IssueListServiceResponse(services.ServiceResponseList[Issue]):
    """Issue List Service Response Schema"""


class RelateDeviceResponse(api.ApiResponse[tuple[IssueId, devices.DeviceId]]):
    """"""
