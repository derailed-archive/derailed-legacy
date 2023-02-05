use authgrpc::authorization_server::{Authorization, AuthorizationServer};
use authgrpc::{CreateToken, NewToken, Valid, ValidateToken};
use base64::{engine::general_purpose, Engine as _};
use itsdangerous::{default_builder, IntoTimestampSigner, TimestampSigner};
use tonic::{transport::Server, Request, Response, Status};

mod authgrpc {
    tonic::include_proto!("derailed.grpc.auth");
}

#[derive(Default)]
struct DynamicAuthorization {}

#[tonic::async_trait]
impl Authorization for DynamicAuthorization {
    async fn create(&self, request: Request<CreateToken>) -> Result<Response<NewToken>, Status> {
        let d = request.into_inner();
        let signer = default_builder(d.password).build().into_timestamp_signer();

        Ok(Response::new(NewToken {
            token: signer.sign(general_purpose::URL_SAFE.encode(&d.user_id)),
        }))
    }

    async fn validate(&self, request: Request<ValidateToken>) -> Result<Response<Valid>, Status> {
        let d = request.into_inner();
        let signer = default_builder(d.password).build().into_timestamp_signer();

        let unsigned = signer.unsign(&d.token);

        if unsigned.is_err() {
            return Ok(Response::new(Valid { valid: false }));
        } else {
            let user_id = unsigned.unwrap().value().to_string();

            match general_purpose::URL_SAFE.decode(user_id) {
                Ok(v) => {
                    let value = std::str::from_utf8(v.as_slice()).unwrap();

                    return Ok(Response::new(Valid {
                        valid: value == d.user_id,
                    }));
                }
                Err(_) => return Ok(Response::new(Valid { valid: false })),
            }
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // as followed with default ports:
    // guilds grpc: 50051
    // users grpc: 50052
    // auth grpc: 50053
    let addr = "[::1]:50053".parse().unwrap();
    let authorizer = DynamicAuthorization::default();

    println!("Starting up gRPC auth on port 50053");

    Server::builder()
        .add_service(AuthorizationServer::new(authorizer))
        .serve(addr)
        .await?;

    Ok(())
}
