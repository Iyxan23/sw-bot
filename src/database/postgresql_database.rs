use crate::database::{IDatabase, MemberMsgCount};
use std::collections::HashMap;
use serenity::model::id::UserId;
use tokio_postgres::{NoTls, Socket};
use tokio_postgres::tls::NoTlsStream;
use std::env;
use async_trait::async_trait;

struct PostgreSQLDatabase {
    client: tokio_postgres::Client,
    connection: tokio_postgres::Connection<Socket, NoTlsStream>,
}

unsafe impl Sync for PostgreSQLDatabase {}

impl PostgreSQLDatabase {
    async fn new() -> Self {
        let postgres_credentials =
            env::var("POSTGRES_CREDENTIALS")
                .expect("POSTGRES_CREDENTIALS environment variable is not present");

        let (client, connection) =
            tokio_postgres::connect(postgres_credentials.as_str(), NoTls)
                .await
                .expect("Cannot connect to the PostgreSQL database");

        PostgreSQLDatabase {
            client, connection
        }
    }
}

#[async_trait]
impl IDatabase for PostgreSQLDatabase {
    async fn init(&self) {
        // create table(s) if they doesn't exist
        self.client
            .execute("CREATE TABLE IF NOT EXISTS msg_count ( \
                    user_id BIGINT NOT NULL, \
                    count INT NOT NULL DEFAULT '0', \
                )", &[])
            .await
            .expect("Cannot create the table msg_count");
    }

    async fn list_active_members(&self) -> Vec<MemberMsgCount> {
        let mut active_members = Vec::new();

        let rows =
            self.client
                .query("SELECT * FROM msg_count ORDER BY count DESC LIMIT 10", &[])
                .await
                .expect("Failed to prepare the \"list active members\" statement");

        for row in rows {
            let user_id: UserId = {
                let user_id_signed: i64 = row.get(0);
                UserId(user_id_signed as u64)
            };

            let count: i32 = row.get(1);

            active_members.push(MemberMsgCount {
                user_id,
                count: (count as u32)
            });
        }

        return active_members;
    }

    async fn commit_msg_count(&self, batch: HashMap<UserId, u32>) {
        todo!()
    }

    async fn get_msg_count(&self, user: UserId) -> u32 {
        todo!()
    }
}