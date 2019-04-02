from django.conf import settings

from importlib import import_module

from .serializers import (
    LoginSerializer as DefaultLoginSerializer,
    APIKeyLoginSerializer as DefaultAPIKeyLoginSerializer,
    GAVerifySerializer as DefaultGAVerifySerializer,
    DuoVerifySerializer as DefaultDuoVerifySerializer,
    YubikeyOTPVerifySerializer as DefaultYubikeyOTPVerifySerializer,
    ActivateTokenSerializer as DefaultActivateTokenSerializer,
    LogoutSerializer as DefaultLogoutSerializer,
    VerifyEmailSerializeras as DefaultVerifyEmailSerializer,
    RegisterSerializer as DefaultRegisterSerializer,
    UserSearchSerializer as DefaultUserSearchSerializer,
    ReadSecretHistorySerializer as DefaultReadSecretHistorySerializer,
    ReadHistorySerializer as DefaultReadHistorySerializer,
    UserUpdateSerializer as DefaultUserUpdateSerializer,
    UserDeleteSerializer as DefaultUserDeleteSerializer,
    NewGASerializer as DefaultNewGASerializer,
    NewDuoSerializer as DefaultNewDuoSerializer,
    NewYubikeyOTPSerializer as DefaultNewYubikeyOTPSerializer,
    ActivateYubikeySerializer as DefaultActivateYubikeySerializer,
    DeleteYubikeySerializer as DefaultDeleteYubikeySerializer,
    ActivateGASerializer as DefaultActivateGASerializer,
    DeleteGASerializer as DefaultDeleteGASerializer,
    ActivateDuoSerializer as DefaultActivateDuoSerializer,
    DeleteDuoSerializer as DefaultDeleteDuoSerializer,
    CreateShareRightSerializer as DefaultCreateShareRightSerializer,
    UpdateShareRightSerializer as DefaultUpdateShareRightSerializer,
    DeleteShareRightSerializer as DefaultDeleteShareRightSerializer,
    CreateRecoverycodeSerializer as DefaultCreateRecoverycodeSerializer,
    CreateEmergencycodeSerializer as DefaultCreateEmergencycodeSerializer,
    EmergencyLoginSerializer as DefaultEmergencyLoginSerializer,
    ActivateEmergencyLoginSerializer as DefaultActivateEmergencyLoginSerializer,
    DeleteEmergencycodeSerializer as DefaultDeleteEmergencycodeSerializer,
    EnableNewPasswordSerializer as DefaultEnableNewPasswordSerializer,
    SetNewPasswordSerializer as DefaultSetNewPasswordSerializer,
    CreateShareLinkSerializer as DefaultCreateShareLinkSerializer,
    UpdateShareLinkSerializer as DefaultUpdateShareLinkSerializer,
    DeleteShareLinkSerializer as DefaultDeleteShareLinkSerializer,
    CreateShareSerializer as DefaultCreateShareSerializer,
    UpdateShareSerializer as DefaultUpdateShareSerializer,
    CreateFileSerializer as DefaultCreateFileSerializer,
    ReadFileSerializer as DefaultReadFileSerializer,
    DatastoreOverviewSerializer as DefaultDatastoreOverviewSerializer,
    CreateDatastoreSerializer as DefaultCreateDatastoreSerializer,
    UpdateDatastoreSerializer as DefaultUpdateDatastoreSerializer,
    DeleteDatastoreSerializer as DefaultDeleteDatastoreSerializer,
    DeleteMembershipSerializer as DefaultDeleteMembershipSerializer,
    ShareOverviewSerializer as DefaultShareOverviewSerializer,
    ShareRightAcceptSerializer as DefaultShareRightAcceptSerializer,
    ShareRightDeclineSerializer as DefaultShareRightDeclineSerializer,
    MoveSecretLinkSerializer as DefaultMoveSecretLinkSerializer,
    DeleteSecretLinkSerializer as DefaultDeleteSecretLinkSerializer,
    MoveFileLinkSerializer as DefaultMoveFileLinkSerializer,
    DeleteFileLinkSerializer as DefaultDeleteFileLinkSerializer,
    CreateGroupSerializer as DefaultCreateGroupSerializer,
    ReadGroupRightsSerializer as DefaultReadGroupRightsSerializer,
    CreateSecretSerializer as DefaultCreateSecretSerializer,
    UpdateSecretSerializer as DefaultUpdateSecretSerializer,
    CreateMembershipSerializer as DefaultCreateMembershipSerializer,
    UpdateMembershipSerializer as DefaultUpdateMembershipSerializer,
    UpdateGroupSerializer as DefaultUpdateGroupSerializer,
    DeleteGroupSerializer as DefaultDeleteGroupSerializer,
    MembershipAcceptSerializer as DefaultMembershipAcceptSerializer,
    MembershipDeclineSerializer as DefaultMembershipDeclineSerializer,
    CreateAPIKeySerializer as DefaultCreateAPIKeySerializer,
    UpdateAPIKeySerializer as DefaultUpdateAPIKeySerializer,
    ReadSecretWithAPIKeySerializer as DefaultReadSecretWithAPIKeySerializer,
    DeleteAPIKeySerializer as DefaultDeleteAPIKeySerializer,
    AddSecretToAPIKeySerializer as DefaultAddSecretToAPIKeySerializer,
    RemoveSecretFromAPIKeySerializer as DefaultRemoveSecretFromAPIKeySerializer,
    ReadShardSerializer as DefaultReadShardSerializer,
    CreateFileRepositorySerializer as DefaultCreateFileRepositorySerializer,
    UpdateFileRepositorySerializer as DefaultUpdateFileRepositorySerializer,
    DeleteFileRepositorySerializer as DefaultDeleteFileRepositorySerializer,
    FileRepositoryUploadSerializer as DefaultFileRepositoryUploadSerializer,
    FileRepositoryDownloadSerializer as DefaultFileRepositoryDownloadSerializer,
    FileRepositoryRightAcceptSerializer as DefaultFileRepositoryRightAcceptSerializer,
    FileRepositoryRightDeclineSerializer as DefaultFileRepositoryRightDeclineSerializer,
    CreateFileRepositoryRightSerializer as DefaultCreateFileRepositoryRightSerializer,
    UpdateFileRepositoryRightSerializer as DefaultUpdateFileRepositoryRightSerializer,
    DeleteFileRepositoryRightSerializer as DefaultDeleteFileRepositoryRightSerializer,
)

def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)

serializers = getattr(settings, 'RESTAPI_AUTH_SERIALIZERS', {})

LoginSerializer = import_callable(
    serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer)
)
APIKeyLoginSerializer = import_callable(
    serializers.get('API_KEY_LOGIN_SERIALIZER', DefaultAPIKeyLoginSerializer)
)

GAVerifySerializer = import_callable(
    serializers.get('GA_VERIFY_SERIALIZER', DefaultGAVerifySerializer)
)

DuoVerifySerializer = import_callable(
    serializers.get('DUO_VERIFY_SERIALIZER', DefaultDuoVerifySerializer)
)

YubikeyOTPVerifySerializer = import_callable(
    serializers.get('YUBIKEY_OTP_VERIFY_SERIALIZER', DefaultYubikeyOTPVerifySerializer)
)

ActivateTokenSerializer = import_callable(
    serializers.get('ACTIVATE_TOKEN_SERIALIZER', DefaultActivateTokenSerializer)
)

LogoutSerializer = import_callable(
    serializers.get('LOGOUT_SERIALIZER', DefaultLogoutSerializer)
)


RegisterSerializer = import_callable(
    serializers.get(
        'REGISTER_SERIALIZER',
        DefaultRegisterSerializer
    )
)


VerifyEmailSerializer = import_callable(
    serializers.get(
        'VERIFY_EMAIL_SERIALIZER',
        DefaultVerifyEmailSerializer
    )
)


UserSearchSerializer = import_callable(
    serializers.get(
        'USER_SEARCH_SERIALIZER',
        DefaultUserSearchSerializer
    )
)


ReadSecretHistorySerializer = import_callable(
    serializers.get(
        'READ_SECRET_HISTORY_SERIALIZER',
        DefaultReadSecretHistorySerializer
    )
)


ReadHistorySerializer = import_callable(
    serializers.get(
        'READ_HISTORY_SERIALIZER',
        DefaultReadHistorySerializer
    )
)

UserUpdateSerializer = import_callable(
    serializers.get(
        'USER_UPDATE_SERIALIZER',
        DefaultUserUpdateSerializer
    )
)

UserDeleteSerializer = import_callable(
    serializers.get(
        'USER_DELETE_SERIALIZER',
        DefaultUserDeleteSerializer
    )
)

NewGASerializer = import_callable(
    serializers.get(
        'NEW_GA_SERIALIZER',
        DefaultNewGASerializer
    )
)

NewDuoSerializer = import_callable(
    serializers.get(
        'NEW_DUO_SERIALIZER',
        DefaultNewDuoSerializer
    )
)

NewYubikeyOTPSerializer = import_callable(
    serializers.get(
        'NEW_YUBIKEY_OTP_SERIALIZER',
        DefaultNewYubikeyOTPSerializer
    )
)

ActivateYubikeySerializer = import_callable(
    serializers.get(
        'ACTIVATE_YUBIKEY_SERIALIZER',
        DefaultActivateYubikeySerializer
    )
)

DeleteYubikeySerializer = import_callable(
    serializers.get(
        'DELETE_YUBIKEY_SERIALIZER',
        DefaultDeleteYubikeySerializer
    )
)

ActivateGASerializer = import_callable(
    serializers.get(
        'ACTIVATE_GA_SERIALIZER',
        DefaultActivateGASerializer
    )
)

DeleteGASerializer = import_callable(
    serializers.get(
        'DELETE_GA_SERIALIZER',
        DefaultDeleteGASerializer
    )
)

ActivateDuoSerializer = import_callable(
    serializers.get(
        'ACTIVATE_DUO_SERIALIZER',
        DefaultActivateDuoSerializer
    )
)

DeleteDuoSerializer = import_callable(
    serializers.get(
        'DELETE_DUO_SERIALIZER',
        DefaultDeleteDuoSerializer
    )
)


CreateShareRightSerializer = import_callable(
    serializers.get(
        'CREATE_SHARE_RIGHT_SERIALIZER',
        DefaultCreateShareRightSerializer
    )
)

UpdateShareRightSerializer = import_callable(
    serializers.get(
        'UPDATE_SHARE_RIGHT_SERIALIZER',
        DefaultUpdateShareRightSerializer
    )
)

DeleteShareRightSerializer = import_callable(
    serializers.get(
        'DELETE_SHARE_RIGHT_SERIALIZER',
        DefaultDeleteShareRightSerializer
    )
)


CreateRecoverycodeSerializer = import_callable(
    serializers.get(
        'CREATE_RECOVERYCODE_SERIALIZER',
        DefaultCreateRecoverycodeSerializer
    )
)


CreateEmergencycodeSerializer = import_callable(
    serializers.get(
        'CREATE_EMERGENCYCODE_SERIALIZER',
        DefaultCreateEmergencycodeSerializer
    )
)


EmergencyLoginSerializer = import_callable(
    serializers.get(
        'EMERGENCY_LOGIN_SERIALIZER',
        DefaultEmergencyLoginSerializer
    )
)


ActivateEmergencyLoginSerializer = import_callable(
    serializers.get(
        'ACTIVATE_EMERGENCY_LOGIN_SERIALIZER',
        DefaultActivateEmergencyLoginSerializer
    )
)


DeleteEmergencycodeSerializer = import_callable(
    serializers.get(
        'DELETE_EMERGENCYCODE_SERIALIZER',
        DefaultDeleteEmergencycodeSerializer
    )
)


EnableNewPasswordSerializer = import_callable(
    serializers.get(
        'ENABLE_NEW_PASSWORD_SERIALIZER',
        DefaultEnableNewPasswordSerializer
    )
)


SetNewPasswordSerializer = import_callable(
    serializers.get(
        'SET_NEW_PASSWORD_SERIALIZER',
        DefaultSetNewPasswordSerializer
    )
)

CreateShareLinkSerializer = import_callable(
    serializers.get(
        'CREATE_SHARE_LINK_SERIALIZER',
        DefaultCreateShareLinkSerializer
    )
)

UpdateShareLinkSerializer = import_callable(
    serializers.get(
        'UPDATE_SHARE_LINK_SERIALIZER',
        DefaultUpdateShareLinkSerializer
    )
)

DeleteShareLinkSerializer = import_callable(
    serializers.get(
        'DELETE_SHARE_LINK_SERIALIZER',
        DefaultDeleteShareLinkSerializer
    )
)


CreateShareSerializer = import_callable(
    serializers.get(
        'CREATE_SHARE_SERIALIZER',
        DefaultCreateShareSerializer
    )
)


UpdateShareSerializer = import_callable(
    serializers.get(
        'UPDATE_SHARE_SERIALIZER',
        DefaultUpdateShareSerializer
    )
)


CreateFileSerializer = import_callable(
    serializers.get(
        'CREATE_FILE_SERIALIZER',
        DefaultCreateFileSerializer
    )
)


ReadFileSerializer = import_callable(
    serializers.get(
        'READ_FILE_SERIALIZER',
        DefaultReadFileSerializer
    )
)

DatastoreOverviewSerializer = import_callable(
    serializers.get(
        'DATASTORE_OVERVIEW_SERIALIZER',
        DefaultDatastoreOverviewSerializer
    )
)

CreateDatastoreSerializer = import_callable(
    serializers.get(
        'CREATE_DATASTORE_SERIALIZER',
        DefaultCreateDatastoreSerializer
    )
)

UpdateDatastoreSerializer = import_callable(
    serializers.get(
        'UPDATE_DATASTORE_SERIALIZER',
        DefaultUpdateDatastoreSerializer
    )
)

DeleteDatastoreSerializer = import_callable(
    serializers.get(
        'DELETE_DATASTORE_SERIALIZER',
        DefaultDeleteDatastoreSerializer
    )
)


DeleteMembershipSerializer = import_callable(
    serializers.get(
        'DELETE_MEMBERSHIP_SERIALIZER',
        DefaultDeleteMembershipSerializer
    )
)

ShareOverviewSerializer = import_callable(
    serializers.get(
        'SHARE_OVERVIEW_SERIALIZER',
        DefaultShareOverviewSerializer
    )
)

ShareRightAcceptSerializer = import_callable(
    serializers.get(
        'SHARE_RIGHT_ACCEPT_SERIALIZER',
        DefaultShareRightAcceptSerializer
    )
)

ShareRightDeclineSerializer = import_callable(
    serializers.get(
        'SHARE_RIGHT_DECLINE_SERIALIZER',
        DefaultShareRightDeclineSerializer
    )
)

MoveSecretLinkSerializer = import_callable(
    serializers.get(
        'MOVE_SECRET_LINK_SERIALIZER',
        DefaultMoveSecretLinkSerializer
    )
)

DeleteSecretLinkSerializer = import_callable(
    serializers.get(
        'DELETE_SECRET_LINK_SERIALIZER',
        DefaultDeleteSecretLinkSerializer
    )
)

MoveFileLinkSerializer = import_callable(
    serializers.get(
        'MOVE_FILE_LINK_SERIALIZER',
        DefaultMoveFileLinkSerializer
    )
)

DeleteFileLinkSerializer = import_callable(
    serializers.get(
        'DELETE_FILE_LINK_SERIALIZER',
        DefaultDeleteFileLinkSerializer
    )
)

CreateGroupSerializer = import_callable(
    serializers.get(
        'CREATE_GROUP_SERIALIZER',
        DefaultCreateGroupSerializer
    )
)

ReadGroupRightsSerializer = import_callable(
    serializers.get(
        'READ_GROUP_RIGHTS_SERIALIZER',
        DefaultReadGroupRightsSerializer
    )
)

CreateSecretSerializer = import_callable(
    serializers.get(
        'CREATE_SECRET_SERIALIZER',
        DefaultCreateSecretSerializer
    )
)

UpdateSecretSerializer = import_callable(
    serializers.get(
        'UPDATE_SECRET_SERIALIZER',
        DefaultUpdateSecretSerializer
    )
)

CreateMembershipSerializer = import_callable(
    serializers.get(
        'CREATE_MEMBERSHIP_SERIALIZER',
        DefaultCreateMembershipSerializer
    )
)

UpdateMembershipSerializer = import_callable(
    serializers.get(
        'CREATE_MEMBERSHIP_SERIALIZER',
        DefaultUpdateMembershipSerializer
    )
)

UpdateGroupSerializer = import_callable(
    serializers.get(
        'UPDATE_GROUP_SERIALIZER',
        DefaultUpdateGroupSerializer
    )
)

DeleteGroupSerializer = import_callable(
    serializers.get(
        'DELETE_GROUP_SERIALIZER',
        DefaultDeleteGroupSerializer
    )
)

MembershipAcceptSerializer = import_callable(
    serializers.get(
        'MEMBERSHIP_ACCEPT_SERIALIZER',
        DefaultMembershipAcceptSerializer
    )
)

MembershipDeclineSerializer = import_callable(
    serializers.get(
        'MEMBERSHIP_DECLINE_SERIALIZER',
        DefaultMembershipDeclineSerializer
    )
)

CreateAPIKeySerializer = import_callable(
    serializers.get(
        'CREATE_API_KEY_SERIALIZER',
        DefaultCreateAPIKeySerializer
    )
)

UpdateAPIKeySerializer = import_callable(
    serializers.get(
        'UPDATE_API_KEY_SERIALIZER',
        DefaultUpdateAPIKeySerializer
    )
)

ReadSecretWithAPIKeySerializer = import_callable(
    serializers.get(
        'READ_SECRET_WITH_API_KEY_SERIALIZER',
        DefaultReadSecretWithAPIKeySerializer
    )
)

DeleteAPIKeySerializer = import_callable(
    serializers.get(
        'DELETE_API_KEY_SERIALIZER',
        DefaultDeleteAPIKeySerializer
    )
)

AddSecretToAPIKeySerializer = import_callable(
    serializers.get(
        'ADD_SECRET_TO_API_KEY_SERIALIZER',
        DefaultAddSecretToAPIKeySerializer
    )
)

RemoveSecretFromAPIKeySerializer = import_callable(
    serializers.get(
        'REMOVE_SECRET_FROM_API_KEY_SERIALIZER',
        DefaultRemoveSecretFromAPIKeySerializer
    )
)


ReadShardSerializer = import_callable(
    serializers.get(
        'READ_SHARD_SERIALIZER',
        DefaultReadShardSerializer
    )
)

CreateFileRepositorySerializer = import_callable(
    serializers.get(
        'CREATE_FILE_REPOSITORY_SERIALIZER',
        DefaultCreateFileRepositorySerializer
    )
)

UpdateFileRepositorySerializer = import_callable(
    serializers.get(
        'UPDATE_FILE_REPOSITORY_SERIALIZER',
        DefaultUpdateFileRepositorySerializer
    )
)

DeleteFileRepositorySerializer = import_callable(
    serializers.get(
        'DELETE_FILE_REPOSITORY_SERIALIZER',
        DefaultDeleteFileRepositorySerializer
    )
)

FileRepositoryUploadSerializer = import_callable(
    serializers.get(
        'FILE_REPOSITORY_UPLOAD_SERIALIZER',
        DefaultFileRepositoryUploadSerializer
    )
)

FileRepositoryDownloadSerializer = import_callable(
    serializers.get(
        'FILE_REPOSITORY_DOWNLOAD_SERIALIZER',
        DefaultFileRepositoryDownloadSerializer
    )
)

FileRepositoryRightAcceptSerializer = import_callable(
    serializers.get(
        'FILE_REPOSITORY_RIGHT_ACCEPT_SERIALIZER',
        DefaultFileRepositoryRightAcceptSerializer
    )
)

FileRepositoryRightDeclineSerializer = import_callable(
    serializers.get(
        'FILE_REPOSITORY_RIGHT_DECLINE_SERIALIZER',
        DefaultFileRepositoryRightDeclineSerializer
    )
)

CreateFileRepositoryRightSerializer = import_callable(
    serializers.get(
        'CREATE_FILE_REPOSITORY_RIGHT_SERIALIZER',
        DefaultCreateFileRepositoryRightSerializer
    )
)

UpdateFileRepositoryRightSerializer = import_callable(
    serializers.get(
        'CREATE_FILE_REPOSITORY_RIGHT_SERIALIZER',
        DefaultUpdateFileRepositoryRightSerializer
    )
)


DeleteFileRepositoryRightSerializer = import_callable(
    serializers.get(
        'DELETE_FILE_REPOSITORY_RIGHT_SERIALIZER',
        DefaultDeleteFileRepositoryRightSerializer
    )
)


EMAIL_VERIFICATION = 'mandatory'
