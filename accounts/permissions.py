from rest_framework.permissions import BasePermission


class IsHR(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and hasattr(
                request.user,
                "userprofile"
            )
            and request.user.userprofile.role
            == "hr"
        )


class IsFinance(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and hasattr(
                request.user,
                "userprofile"
            )
            and request.user.userprofile.role
            == "finance"
        )


class IsAdmin(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user.is_authenticated
            and hasattr(
                request.user,
                "userprofile"
            )
            and request.user.userprofile.role
            == "admin"
        )