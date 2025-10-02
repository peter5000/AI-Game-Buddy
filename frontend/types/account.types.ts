export interface User {
    userId: string;
    username: string;
    email: string;
}

export interface SignupRequest {
    username: string;
    email: string;
    password: string;
}

export interface SigninRequest {
    identifier: string;
    password: string;
}
