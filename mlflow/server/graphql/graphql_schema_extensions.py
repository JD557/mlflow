import graphene

import mlflow
from mlflow.server.graphql.autogenerated_graphql_schema import (
    MlflowExperiment,
    MlflowRun,
    MutationType,
    QueryType,
)
from mlflow.utils.proto_json_utils import parse_dict


class Test(graphene.ObjectType):
    output = graphene.String(description="Echoes the input string")


class TestMutation(graphene.ObjectType):
    output = graphene.String(description="Echoes the input string")


class MlflowRunExtension(MlflowRun):
    experiment = graphene.Field(MlflowExperiment)

    def resolve_experiment(self, info):
        experiment_id = self.info.experiment_id
        input_dict = {"experiment_id": experiment_id}
        request_message = mlflow.protos.service_pb2.GetExperiment()
        parse_dict(input_dict, request_message)
        return mlflow.server.handlers.get_experiment_impl(request_message).experiment


class Query(QueryType):
    test = graphene.Field(Test, input_string=graphene.String(), description="Simple echoing field")

    def resolve_test(self, info, input_string):
        return {"output": input_string}


class Mutation(MutationType):
    testMutation = graphene.Field(
        TestMutation, input_string=graphene.String(), description="Simple echoing field"
    )

    def resolve_test_mutation(self, info, input_string):
        return {"output": input_string}


schema = graphene.Schema(query=Query, mutation=Mutation)